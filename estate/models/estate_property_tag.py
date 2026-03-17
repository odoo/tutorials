from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate property tags'

    name = fields.Char('Name', required=True)
    