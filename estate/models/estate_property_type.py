from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of a property'

    name = fields.Char('Property Type', required=True)