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
        tracking=True
    )
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', 
        string="Property Type", 
    )
    salesperson_id = fields.Many2one(
        related='property_id.salesperson_id',
        string="SalesPerson",
    )

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'An offer price must be strictly positive.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        result = super(EstatePropertyOffer, self).create(vals_list)
        # Ensure the offer amount is higher than existing offers
        for offer, vals in zip(result, vals_list):
            property_id = offer.property_id.id
            if offer.property_id.state == 'new':
               offer.property_id.state = 'offer_received'
            elif offer.property_id.best_price > vals.get('price'):
                    raise UserError(f"Offer amount must be higher than the existing offer of {offer.property_id.best_price}.")
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
            elif offer.property_id.state == 'cancelled':
                raise UserError("The property has been cancelled, you cannot accept an offer.")  
            offer.update({
              'status': 'accepted',
            })
            offer.property_id.write({
              'state': 'offer_accepted',
              'selling_price': offer.price,
              'buyer_id': offer.partner_id.id,
            })
        other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("You cannot refuse an offer that has already been accepted.")
            offer.status = 'refused'
