from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tags'
    _order = 'name'

    name = fields.Char(string="Property Tags", required=True)
    color = fields.Char(string="Color")

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'A property tag name must be unique.')
    ]
