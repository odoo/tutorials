from odoo import models, fields


class EstateType(models.Model):
    _name = 'estate.type'
    _description = 'Estate Type'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many('estate', 'estate_type_id', string='Properties')

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A property type name must be unique.",
    )
