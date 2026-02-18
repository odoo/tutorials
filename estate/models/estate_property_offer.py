from odoo import models, fields, api, exceptions
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for a specific property, made by a specific buyer at lower or higher price than the expected price"
    _check_price = models.Constraint('CHECK(price >= 0)', 'The price must be positive!')

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

    def offer_accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    raise exceptions.UserError('An offer was already accepted for this property!')
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True
        
    def offer_refuse(self):
        for record in self:
            record.status = 'refused'
        return True