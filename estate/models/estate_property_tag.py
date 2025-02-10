from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag model'

    name = fields.Char(string='Title')

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)', 'Property tag must be unique.')
    ]
