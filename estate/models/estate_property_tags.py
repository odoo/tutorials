from odoo import models, fields


class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Tags'

    name = fields.Char()