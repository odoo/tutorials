from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = "name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')
