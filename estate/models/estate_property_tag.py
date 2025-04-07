from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = 'Estate Property Tag'

    name = fields.Char(string='Title', required=True)

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)', 'Property tag must be unique.')
    ]
