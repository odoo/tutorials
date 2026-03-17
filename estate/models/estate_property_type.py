from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The types available for properties/real estates'

    name = fields.Char('Name', required=True)
    