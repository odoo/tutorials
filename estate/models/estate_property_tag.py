from odoo import fields, models


class EstateTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'It allows to create a new property tag'

    name = fields.Char(required=True)
