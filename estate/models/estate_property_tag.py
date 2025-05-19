from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(string='Title', required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)', 'Property tag must be unique.')
    ]
