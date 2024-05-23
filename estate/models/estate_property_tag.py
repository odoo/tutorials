from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "estate properties tags"

    name = fields.Char(required=True)
