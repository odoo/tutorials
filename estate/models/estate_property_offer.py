from odoo import api, models, fields
from datetime import timedelta,datetime
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('cancelled', 'cancelled')
    ], string='Status')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    validity=fields.Integer(string="validity", default=7)
    date_deadline=fields.Date(string="date_deadline", compute="compute_date_deadline", inverse="inverse_date_deadline" , store="true")

    @api.depends('create_date', 'validity')
    def compute_date_deadline(self):
        for record in self:
            if record.create_date:
                # Compute the deadline by adding the validity (days) to the creation date
                record.date_deadline = (record.create_date.date() + timedelta(days=record.validity))
     

    def inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model
    def action_accept(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError('This offer has already been accepted.')
            
            # Set the property to sold and update buyer and selling price
            property = offer.property_id
            if property.state == 'sold':
                raise UserError('The property is already sold.')
            property.selling_price = offer.price
            property.buyer_id = offer.partner_id
            property.state = 'sold'
            
            offer.status = 'accepted'
            pass

    @api.model
    def action_refuse(self):
        for offer in self:
            if offer.status == 'refused':
                raise UserError('This offer has already been refused.')
            offer.status = 'refused'
            pass