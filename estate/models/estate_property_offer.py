"""docstring property offer"""

from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    status = fields.Selection(selection=[("awaiting", "Awaiting"), ("refused", "Refused"), ("accepted", "Accepted")], required=True, default="awaiting", copy=False)

    property_id = fields.Many2one("estate.property", required=True)
