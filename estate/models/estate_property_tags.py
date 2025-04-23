from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'property tags'

    name = fields.Char(required = True)