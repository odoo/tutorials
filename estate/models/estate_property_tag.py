from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'The property Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer("Color")
    _sql_constraints = [('tag_name_unique', 'UNIQUE(name)', "The tag name must be unique.")]
