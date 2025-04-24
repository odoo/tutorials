from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate type model"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)

    # One2Many relationships
    property_ids = fields.One2many('estate.property', 'property_type_id')
