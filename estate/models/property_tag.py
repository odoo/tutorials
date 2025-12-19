from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char("Tag Name", required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The property tag name must be unique'
    )
