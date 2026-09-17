from odoo import fields, models


class Type(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of property of Estate'

    name = fields.Char(required=True)
