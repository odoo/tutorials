from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "describes the type of a property"

    name = fields.Char(required=True)
    _sql_constraints = [('name_unique', 'unique(name)', 'A property type name must be unique')]