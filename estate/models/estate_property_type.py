from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string = 'Property Type',required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
