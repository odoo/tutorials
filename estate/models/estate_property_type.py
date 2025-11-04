from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _order = "sequence"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(string="Sequence", default=1)

    _unique_name = models.Constraint(
    'UNIQUE(name)',
    'name already exists!',
    )
