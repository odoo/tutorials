from odoo import fields, models


class EstatePropertyTagModel(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'

    name = fields.Char('Title', required=True, translate=True)
