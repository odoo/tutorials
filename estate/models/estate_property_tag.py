from odoo import fields, models


class Type(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag of property of Estate'

    name = fields.Char(required=True)
