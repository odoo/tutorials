from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name'

    name = fields.Char(required=True)

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _unique_property_type_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.',
    )
