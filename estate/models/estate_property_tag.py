from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Type'
    _order = 'name asc'

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_unique_name = models.Constraint(
        "UNIQUE(name)", "A property tag name should be unique",
    )
