from odoo import fields, models


class EstatePropertyAddress(models.Model):
    _name = "estate.property.address"
    _description = "Estate Property Address"

    street = fields.Char()
    city = fields.Char()
    country = fields.Char()
