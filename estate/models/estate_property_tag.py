from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag an estate property'

    name = fields.Char(required=True)
    