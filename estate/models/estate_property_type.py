from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    property_type = fields.Many2one("estate.property")
    buyer = fields.Many2one("res.partner")
    seller = fields.Many2one("res.partner")
