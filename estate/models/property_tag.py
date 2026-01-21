from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate_property_tag'
    _description = 'estate property tag'

    name = fields.Char(required=True)
