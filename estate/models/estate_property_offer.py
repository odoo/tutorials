# estate/models/estate_property_offer.py
from odoo import models, fields, api
from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _inherit = 'estate.property.offer'
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(string="Status", required=True, selection=[("accepted", "Accepted"), ("refused", "Refused")], default="refused")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    state = fields.Selection(selection_add=[('accepted', 'Accepted'), ('refused', 'Refused')])
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)

@api.model
def create(self, vals):
        
    return super(EstatePropertyOffer, self).create(vals)

def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days

def accept_offer(self):
        if self.state == 'efused':
            raise UserError("An offer that has been refused cannot be accepted")
        self.state = 'accepted'
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price

def refuse_offer(self):
        if self.state == 'accepted':
            raise UserError("An offer that has been accepted cannot be refused")
        self.state = 'refused'


class Offer(models.Model):
    _name = 'offer'
    price = fields.Float(string='Price')

    _sql_constraints = [
        ('price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive'),
    ]