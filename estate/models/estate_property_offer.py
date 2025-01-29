from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class OfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ('pending', 'Pending')
        ]
    )
    partner_id = fields.Many2one('res.partner', string='Offeror')
    property_id = fields.Many2one('estate_property', string='property')

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Date_deadline', compute="_compute_deadline", inverse="_inverse_deadline")

    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                date_deadline = record.date_deadline
                today = fields.Date.today()
                record.validity = (date_deadline - today).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == "offer accepted":
                raise UserError('An Offer has already been accepted for this property')
            if record.price < record.property_id.expected_price * 0.9:
                raise ValidationError("The price cannot be lower than 90% of the expcted price")
            record.property_id.state = "offer_accepted"
            record.property_id.partner_id = record.partner_id
            record.property_id.selling_price = record.price
            record.status = 'accepted'
    
    def action_refuse_offer(self):
        for record in self:
            record.property_id.partner_id = False  
            record.property_id.selling_price = 0.0 

        record.status = 'refused'

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')

        property_record = self.env['estate.property'].browse(property_id)

        if property_record:
            property_record.state = 'offer_received'
        
        new_offer_price = None
        
        if 'price' in vals:
            new_offer_price = vals['price']

        if new_offer_price is not None:
            existing_offers = self.env['estate_property_offer'].search([
                ('property_id', '=', property_id),
                ('price', '>=', new_offer_price)
            ])
        
        if existing_offers:
                raise UserError(f"The new offer price ({new_offer_price}) is lower than an existing offer.")

        return super().create(vals)



    _sql_constraints = [
        ('check_positive_offer', 'CHECK(price >= 0)',
         'The offer for a real estate should always be positive')
    ]
    