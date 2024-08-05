from odoo import fields, models


class EstatePropertyTypes(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'

    name = fields.Char(required=True)
