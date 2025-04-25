from odoo import fields, models


class EstateTypeModel(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'

    name = fields.Char('Title', required=True, translate=True)
