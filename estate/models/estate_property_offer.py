from odoo import models, fields, api
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for a specific property, made by a specific buyer at lower or higher price than the expected price"

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