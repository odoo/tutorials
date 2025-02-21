from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _sql_constraints = [
        ('check_tag_name', 'unique(name)', 'A property tag name must be unique.')
    ]
    _order = "name"

    name = fields.Char()
    color = fields.Integer()
