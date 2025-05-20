from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "estate property type description"

    name = fields.Char('Property Type', required=True)
