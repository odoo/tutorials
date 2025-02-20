from odoo import models, fields


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'the estate property tag'

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")