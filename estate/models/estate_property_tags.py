from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property Tags'

    name = fields.Char(required=True)
