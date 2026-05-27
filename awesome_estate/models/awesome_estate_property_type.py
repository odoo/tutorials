from odoo import fields, models


class AwesomeEstatePropertyType(models.Model):
    _name = 'awesome.estate.property.type'
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)
