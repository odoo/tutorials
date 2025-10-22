from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "test description"
    _order = "name"

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')

    _check_name = models.Constraint(
        'UNIQUE (name)',
        'The name must be unique',
    )
