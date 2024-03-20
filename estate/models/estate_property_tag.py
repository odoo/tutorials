from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'A property tag'

    name = fields.Char('Name', required=True)
