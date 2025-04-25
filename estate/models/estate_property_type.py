from odoo import fields, models


class EstatePropertyTypeModel(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'

    name = fields.Char('Title', required=True, translate=True)
