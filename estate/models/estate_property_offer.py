from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc" 
    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price >= 1)', 'The offer price must be strictly positive.')
    ]

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'), 
        ('refused', 'Refused')
    ], string="Status" ,copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", related="property_id.property_type_id", store=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date or fields.Date.today(), days=record.validity)
            

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days if record.date_deadline else 0

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_id = self.env['estate.property'].browse(val['property_id'])

            if property_id:
                property_id.write({'state': 'offer_received'})

            if val['price'] < property_id.best_offer:
                raise UserError("Your price is lower than an existing offer.")

        return super(EstatePropertyOffer, self).create(vals)

    def action_accept(self):
        if self.property_id.state == 'offer_accepted':
            raise ValidationError("You can't accept more than one offer")
            
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
