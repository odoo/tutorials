from odoo import models, fields


class PropertyType(models.Model):
    _name = "public.property.type"
    _description = "A different types of properties."
    _order = "name"

    name = fields.Char()
    sequence = fields.Integer()
    property_ids = fields.One2many("public.property", "propertytype_id")
    _sql_constraints = [
        ("uniq_property_type", "unique(name)", "A property type must be unique.")
    ]
