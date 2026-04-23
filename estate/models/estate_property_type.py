from odoo import models, fields


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string="Type", required=True)

    _check_name = models.Constraint(
        'unique(name)'
    )
