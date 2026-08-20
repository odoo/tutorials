from odoo import models, fields


class EstateTag(models.Model):
    _name = 'estate.tag'
    _description = 'Estate Tag'

    name = fields.Char(string='Name', required=True)

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A property tag name must be unique.",
    )
