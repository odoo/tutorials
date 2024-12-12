from odoo import models, fields
from datetime import timedelta
from odoo.exceptions import UserError
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float(string="Offer Price", required=True)
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
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("You cannot accept an offer for a sold property.")
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'sold'
            record.property_id.offer_ids.filtered(lambda o: o.id != record.id).write({'state': 'refused'})
            record.state = 'accepted'

    def action_refuse(self):
        for record in self:
            record.state = 'refused'          
_sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)',
         'The offer price must be strictly positive.')
    ]   


