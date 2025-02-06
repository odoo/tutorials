from odoo import api, fields, models
from datetime import timedelta

class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    _description = "This stores all the offers that are made."

    price = fields.Float(string="Price")
    offer_state = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one("estate.customer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity_days = fields.Integer()
    deadline = fields.Date(compute="_compute_deadline", store=True)

    @api.depends("validity_days")
    def _compute_deadline(self):
        for record in self:
            if record.validity_days:
                record.deadline = fields.Date.today() + timedelta(days=record.validity_days)
