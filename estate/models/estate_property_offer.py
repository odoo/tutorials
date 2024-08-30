from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Price', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('draft', 'Draft')
    ], default='draft', copy=False)
    # state = fields.Selection([
    #     ('accepted', 'Accepted'),
    #     ('refused', 'Refused'),
    #     ('draft', 'Draft')
    # ], default='draft', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True, ondelete='cascade')
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        store=True,
        string='Property Type'
    )
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for offer in self:
            if offer.status == 'accepted':
                raise ValidationError("This offer is already accepted.")
            if offer.status == 'refused':
                raise ValidationError("This offer is refused and cannot be accepted.")
            other_accepted_offers = self.search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted')
            ])
            if other_accepted_offers:
                raise ValidationError("An offer for this property has already been accepted.")
            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            other_offers = self.search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id)
            ])
            other_offers.write({'status': 'refused'})
        return True

    def action_refuse(self):
        for offer in self:
            if offer.status == 'refused':
                raise ValidationError("This offer is already refused.")
            if offer.status == 'accepted':
                raise ValidationError("An accepted offer cannot be refused.")
            offer.status = 'refused'
        return True

    @api.model
    def create(self, vals):

        property_id = self.env['estate.property'].browse(vals['property_id'])
        if property_id.best_price and vals['price'] <= property_id.best_price:
            raise ValidationError("The offer price must be higher than any existing offer.")
        offer = super().create(vals)
        offer.property_id.state = 'offer_received'
        return offer

    def action_confirm_offer(self):
        for offer in self:
            if offer.property_id:
                offer.property_id.write({'state': 'offer_received'})
        self.write({'status': 'accepted'})

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]
