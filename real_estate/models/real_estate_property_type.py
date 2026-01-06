from odoo import fields, models


class RealEstateTag(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(required=True)
