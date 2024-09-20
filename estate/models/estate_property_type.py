from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "sequence, name"

    name = fields.Char("Name", index=True, translate=True)
    property_ids = fields.One2many("estate.property", "property_type_id", "Properties")
    sequence = fields.Integer("Sequence", default=1, help="Used to order estate property types")
