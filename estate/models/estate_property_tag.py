from odoo import fields, models


class EstatePropertytag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Tag names must be unique.')
    ]
