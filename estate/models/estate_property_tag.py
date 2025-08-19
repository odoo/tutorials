from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate properties tags"
    _order = "name"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Each name must be unique.'),
    ]
