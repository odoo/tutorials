from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offers'
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        copy=False,
    )
    amount = fields.Float(string="Offer Amount")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    salesperson_id = fields.Many2one('res.partner', string="Salesperson")
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', 
        string="Property Type", 
        store=True
    )

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'An offer price must be strictly positive.'),
    ]

    @api.model_create_multi
    def create(self, vals):
        result = super(EstatePropertyOffer, self).create(vals)
        # Ensure the offer amount is higher than existing offers
        for offer in result:
            property_id = offer.property_id.id
            offer_amount = offer.amount
            existing_offers = self.env['estate.property.offer'].search([('property_id', '=', property_id)])
            for existing_offer in existing_offers:
                if existing_offer.amount > offer_amount:
                    raise UserError(f"Offer amount must be higher than the existing offer of {existing_offer.amount}.")
        return result

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
          for offer in self:
            if offer.date_deadline:
                if offer.create_date:
                    delta = offer.date_deadline - offer.create_date.date()
                    offer.validity = delta.days
                else:
                    offer.validity = 0

    def action_accept(self):
        property_ids = self.mapped('property_id.id')
        other_offers = self.search([('property_id', 'in', property_ids), ('id', 'not in', self.ids)])
        for offer in self:
             if offer.property_id.state == 'sold':
                 raise UserError("The property has already been sold, you cannot accept an offer.")    
             if offer.property_id.state == 'cancelled':
                 raise UserError("The property has been cancelled, you cannot accept an offer.")            
             offer.status = 'accepted'
             offer.property_id.state = 'offer_accepted'
             offer.property_id.selling_price = offer.price
             offer.property_id.buyer_id = offer.buyer_id
        other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("You cannot refuse an offer that has already been accepted.")
            offer.status = 'refused'

    def write(self, values):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("You cannot edit an offer once it has been accepted.")
        return super(EstatePropertyOffer, self).write(values)
