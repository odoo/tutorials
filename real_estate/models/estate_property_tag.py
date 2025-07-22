from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    _sql_constraints = [
    ('unique_tag_name', 'UNIQUE(name)',
     'Tag name must be unique.'),
    ]

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
    sequence = fields.Integer(string="Sequence", default=10)
