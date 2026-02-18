from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, id"

    name = fields.Char("Name", required=True, translate=True)
    livable = fields.Boolean("Livable", default=True)

    sequence = fields.Integer("Sequence", default=0)
