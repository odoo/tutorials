from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True, string='Property Type')

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price should be strictly positive')
    ]

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

    def action_refused(self):
        for record in self:
            record.status = 'refused'
        return True

    def action_accepted(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError('Sold properties cannot be accepted')
            accepted_offers = record.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted')
            if accepted_offers:
                raise UserError("An offer has already been accepted for this property.")
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    @api.model
    def create(self, values):
        property_id = values.get('property_id')
        if property_id:
            property_name = self.env['estate.property'].browse(property_id)
            new_offer_price = values.get('price', 0)
            highest_offer_price = max(property_name.offer_ids.mapped('price'), default=0)
            if new_offer_price < highest_offer_price:
                raise UserError("Cannot create an offer lower than the existing highest offer.")
            if property_name.state != 'offer_received':
                property_name.state = 'offer_received'
        return super().create(values)
