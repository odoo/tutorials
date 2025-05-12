from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc" 

    price = fields.Float(string = 'Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True, ondelete='cascade')
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Date Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    property_type_id = fields.Many2one(
    "estate.property.type",
    string="Property Type",
    related="property_id.property_type_id",
    store=True)

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.context_today(record)
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            delta = record.date_deadline - create_date.date()
            record.validity = delta.days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state in ['sold', 'cancelled']:
                raise UserError("You cannot accept an offer for a sold or cancelled property.")
            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError("An offer has already been accepted for this property.")
            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
            return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
            return True  # Optional but helps refresh

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        if property_id:
            prop = self.env['estate.property'].browse(property_id)
            # Check for existing higher offers
            existing_offers = self.search([('property_id', '=', property_id)])
            if existing_offers and vals.get('price', 0.0) < max(existing_offers.mapped('price')):
                raise ValidationError("Offer price must exceed existing offers!")
            # Update property state
            if prop.state != 'offer_received':
                prop.write({'state': 'offer_received'})
        return super().create(vals)
