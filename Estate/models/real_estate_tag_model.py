from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    name = fields.Char(required=True)
    color = fields.Integer()

    _order = 'name asc'

    _sql_constraints = [
        ('tag_unique', 'UNIQUE(name)', 'This type of tag already exists.'),
    ]
