from odoo import models, fields, api, exceptions
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for a specific property, made by a specific buyer at lower or higher price than the expected price"
    _check_price = models.Constraint('CHECK(price >= 0)', 'The price must be positive!')
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'), 
            ('refused', 'Refused')
        ], 
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    date_create = fields.Date(default=fields.Date.today)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.date_create + timedelta(days=record.validity)
    
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.date_create).days

    @api.model
    def create(self, vals):
        for record in vals:
            id = record.get('property_id')
            price = record.get('price')
            property = self.env['estate_property'].browse(id)
            if property.offer_ids:
                if price < max(property.offer_ids.mapped('price')):
                    raise exceptions.UserError('New offer price must be higher or equal to the existing offers!')
            property.state = 'offer_received'
        return super().create(vals)

    def offer_accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    raise exceptions.UserError('An offer was already accepted for this property!')
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True
        
    def offer_refuse(self):
        for record in self:
            record.status = 'refused'
        return True