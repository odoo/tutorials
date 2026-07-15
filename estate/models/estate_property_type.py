from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "model for estate property types"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    _name_uniq = models.Constraint(
        'unique(name)',
        "A property type name must be unique.",
    )
