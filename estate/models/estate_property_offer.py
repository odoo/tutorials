from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
        string="Deadline",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != record.id):
                raise UserError(self.env._("Only one offer can be accepted per property."))
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
