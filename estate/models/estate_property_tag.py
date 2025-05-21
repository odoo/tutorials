from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'estate property tag module'

    name = fields.Char(required=True)
