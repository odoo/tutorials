from odoo import models, fields
from datetime import timedelta
from odoo.exceptions import UserError
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'
    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status")
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', 
        string="Property Type", 
        readonly=True
    )
    buyer_id = fields.Many2one(
        'res.partner', 
        string="Buyer", 
        required=True
    )
    seller_id = fields.Many2one(
        'res.partner',
        string="Seller"
    )
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
    def action_accept(self):
        if self.property_id.state == 'sold':
            raise UserError("Cannot accept offers for sold properties.")
        existing_offer = self.search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted')
        ])
        if existing_offer:
            raise UserError("Only one offer can be accepted per property.")
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.env.user.partner_id

    def action_refuse(self):
        if self.status == 'accepted':
            raise UserError("Accepted offers cannot be refused.")
        self.status = 'refused'        
    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)',
         'The offer price must be strictly positive.')
    ]   


