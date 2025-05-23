from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'A tag'
    _order = "name asc"
    _sql_constraints = [
        ('check_unicity', 'UNIQUE (name)', 'A tag with the same name already exists'),
    ]

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')
