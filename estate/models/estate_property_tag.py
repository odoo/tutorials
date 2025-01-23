from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags for our properties'

    name = fields.Char(requird=True)
    
