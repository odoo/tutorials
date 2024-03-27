from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('tag_unique_name', 'unique(name)', 'The tag name must be unique')
    ]
