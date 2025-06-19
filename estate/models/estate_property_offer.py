from odoo import models, fields, api
from datetime import timedelta, date
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    
    validity = fields.Integer("Valid For", default=7, help="Number of days until this offer expires")

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        [
            ('accepted', 'Accepted'), 
            ('refused', 'Refused')
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    
    # Computed fields
    date_deadline = fields.Datetime(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    # Computed functions
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            if record.date_deadline:
                delta = record.date_deadline - create_date
                record.validity = delta.days
                
    # Actions
    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError("You cannot accept an offer on a sold property.")
            if offer.property_id.buyer_id:
                raise UserError("An offer has already been accepted for this property.")

            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"

            # Refuse all other offers
            other_offers = offer.property_id.offer_ids - offer
            other_offers.write({'status': 'refused'})
        return True

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("You cannot refuse an offer that has already been accepted.")
            offer.status = "refused"
        return True
                    
    # SQL Constraints
    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]