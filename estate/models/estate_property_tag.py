from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"
    _name_unique = models.Constraint(
        'unique (name)',
        'A property tag of that name already exists',
    )

    name = fields.Char('Property Tag', required=True)
    color = fields.Integer('Color Index', default=0)
