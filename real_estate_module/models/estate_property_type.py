from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Types such as Home, Apartment, etc"
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id')

    _sql_constraints = [
        (
            'unique_property_type_name',
            'UNIQUE(name)',
            "The name must be unique"
        )
    ]
