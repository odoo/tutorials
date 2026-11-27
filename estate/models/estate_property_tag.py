from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tags'

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer()
