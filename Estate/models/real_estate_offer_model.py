from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    name = fields.Char(required=True)
    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate_property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id')
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    validity = fields.Integer(default=7)

    _order = 'price desc'

    _sql_constraints = [
        ('check_offer', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.status != 'accepted':
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
                record.property_id.state = 'offer_accepted'
            else:
                raise UserError("You can only accept one offer per property.")

    def action_refuse(self):
        for record in self:
            record.status = "refused"
