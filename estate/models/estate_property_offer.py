from odoo import fields, models, api
from odoo.tools.date_utils import add


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for propreties"

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be strictly positive.',
    )
    price = fields.Float(required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    create_date = fields.Date(default=fields.Date.today(), readonly=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    is_available = fields.Boolean(related="property_id.is_available")

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return 1

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return 1
