from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "test description"

    name = fields.Char('Name', required=True)

    _check_name = models.Constraint(
        'UNIQUE (name)',
        'The name must be unique',
    )
