from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Types of estate property'
    
    name = fields.Char(string="Name",required=True)
