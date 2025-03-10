from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", store=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", default="")

    state = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string="Status", default="new")

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def action_accept(self):
        for record in self:
            
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
            return True
            

    def action_refuse(self):
        for record in self:
            record.status = 'canceled'
            return True
    
    def action_sold(self):
        """ Mark offer as sold """
        for record in self:
            record.state = 'sold'

    def action_cancel(self):
        """ Cancel the offer """
        for record in self:
            record.state = 'canceled'