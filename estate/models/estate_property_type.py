from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "describe the type property"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    # SQL constraints
    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'The name of a property type should be unique')
    ]
