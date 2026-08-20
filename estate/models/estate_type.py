from odoo import models, fields


class EstateType(models.Model):
    _name = 'estate.type'
    _description = 'Estate Type'

    name = fields.Char(string='Name', required=True)

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A property type name must be unique.",
    )
