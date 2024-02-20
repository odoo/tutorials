from odoo import api, models, fields
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse="_inverse_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Date.today()
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_property_offer_accepted(self):
        for record in self:
            if record.property_id.selling_price:
                raise UserError("Can't accept more than one offer for a property!")
            record.status = 'accepted'
            record.property_id.selling_price = record.property_id.best_price
            record.property_id.buyer = record.partner_id
        return True

    def action_property_offer_refused(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("Can't refuse an already accepted offer!")
            else:
                record.status = 'refused'
        return True
