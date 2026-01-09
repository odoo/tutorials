from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Defines types of property"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _type_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.',
    )
