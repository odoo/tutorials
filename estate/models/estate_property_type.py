from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = "name"

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'This property type name already exists'
    )

    name = fields.Char(required=True, string='Title')
    sequence = fields.Integer()
    property_ids = fields.One2many("estate.property", "property_type_id")
