from odoo import models, fields

class PropertyTag(models.Model):
    # Model Property
    _name = 'estate.property.tag'
    _description = 'Estate property tags'
    
    # Fields
    name = fields.Char(required=True)
