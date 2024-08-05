from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'real.estate.property.tag'
    _description = 'Property Type'

    name = fields.Char(required=True)