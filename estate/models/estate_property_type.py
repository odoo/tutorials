from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Types for our properties'

    name = fields.Char(requird=True)
    
