from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class OfferModel(models.Model):
    _name = "estate_property_offer"
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
            record.property_id.state = "offer accepted"
            record.property_id.partner_id = record.partner_id
            if record.price < record.property_id.expected_price * 0.9:
                raise ValidationError("The price cannot be lower than 90% of the expcted price")
            record.property_id.selling_price = record.price

        record.status = 'accepted'
    
    def action_refuse_offer(self):
        for record in self:
            record.property_id.partner_id = False  
            record.property_id.selling_price = 0.0 

        record.status = 'refused'

    _sql_constraints = [
        ('check_positive_offer', 'CHECK(price >= 0)',
         'The offer for a real estate should always be positive')
    ]