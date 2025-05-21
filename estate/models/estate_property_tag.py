from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)
