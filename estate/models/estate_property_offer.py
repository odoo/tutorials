from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('draft', 'Draft')
    ], default='draft', copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete='cascade')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("This offer is already accepted.")
            if offer.status == 'refused':
                raise UserError("This offer is refused and cannot be accepted.")
            other_offers = self.search([('property_id', '=', offer.property_id.id), ('status', '=', 'accepted')])
            if other_offers:
                raise UserError("An offer for this property has already been accepted.")
            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
        return True

    def action_refuse(self):
        for offer in self:
            if offer.status == 'refused':
                raise UserError("This offer is already refused.")
            if offer.status == 'accepted':
                raise UserError("An accepted offer cannot be refused.")

            offer.status = 'refused'
        return True
