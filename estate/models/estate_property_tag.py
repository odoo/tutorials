from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char('Name', required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property tag names should be unique'
    )
