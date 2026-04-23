from odoo import models, fields


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string="Type", required=True)

    _check_name = models.Constraint(
        "unique(name)",
    )
