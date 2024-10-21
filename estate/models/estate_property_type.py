from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char("Property type", required=True)

    _sql_constraints = [
        (
            'Unique_property_type_name',
            'UNIQUE(name)',
            'A property type name must be unique'
        )
    ]
