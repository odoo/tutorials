from odoo import models, fields
from datetime import timedelta
from odoo.exceptions import UserError
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'
    price = fields.Float()
    state= fields.Selection([('new', 'New'),('accepted', 'Accepted'), ('refused', 'Refused')], string= "Status" ,default='new')
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status")
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', 
        string="Property Type", 
        readonly=True,
        store=True
    )
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=False)
    seller_id = fields.Many2one('res.partner', string="Salesperson", required=False)
    validity = fields.Integer(string="Validity (days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = (record.date_deadline - record.create_date.date()).days
                record.validity = max(delta, 0)
            else:
                record.validity = 7

    def action_offer_accepted(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status = 'refused'
        return True

    def action_offer_refused(self):
        for record in self:
            record.status = 'refused'
        return True

    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)',
         'The offer price must be strictly positive.')
    ]

    
    @api.model
    def create(self, vals):
        # Ensure property_id exists in vals
        property_id = self.env['estate.property'].browse(vals.get('property_id'))
        if not property_id:
            raise UserError("The property associated with this offer does not exist.")

        # Check if the new offer amount is lower than any existing offers
        existing_offers = self.search([('property_id', '=', property_id.id)])
        for offer in existing_offers:
            if vals.get('price', 0.0) <= offer.price:
                raise UserError(
                    "You cannot create an offer with a price lower than an existing offer."
                )

        # Update the property's state to 'Offer Received'
        property_id.state = 'offer_received'

        # Create the offer as usual
        return super(EstatePropertyOffer, self).create(vals)   


