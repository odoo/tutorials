from odoo import fields, models

class EstateModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate/Property/Offer"

    price = fields.Float(required=True)
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused")
    ])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
