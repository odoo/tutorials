from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag of properties'
    _order = 'name asc'

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [(
        'unique_name', 'unique(name)', "A property tag name must be unique",
    )]
