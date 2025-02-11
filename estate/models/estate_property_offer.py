from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc" 

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'), 
        ('refused', 'Refused')
    ], string="Status" ,copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date or fields.Date.today(), days=record.validity)
            

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days if record.date_deadline else 0

    def action_accept(self):
        for record in self:
            existing_accepted_offer = self.search([
                ('property_id', '=', record.property_id.id),
                ('status', '=', 'accepted')
            ])
            if existing_accepted_offer:
                if(existing_accepted_offer.price < record.price): 
                    existing_accepted_offer.status = 'refused'
                else: raise ValidationError('You already have better accepted offer.')
            
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id.id
            record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price >= 1)', 'The offer price must be strictly positive.')
    ]
