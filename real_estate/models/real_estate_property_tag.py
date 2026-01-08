from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'This are tags used to identify property'

    name = fields.Char(required=True)
