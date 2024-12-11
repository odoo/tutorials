from odoo import models, fields

class estatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Tags'

    name = fields.Char()