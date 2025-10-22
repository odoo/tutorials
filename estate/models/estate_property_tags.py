from odoo import models, fields


class PropertyTypeTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property Tags'
    
    name = fields.Char(string='tags', required=True)
