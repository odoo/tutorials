from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Estate Property Type'

    name = fields.Char(string='Title', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property type must be unique.')
    ]
