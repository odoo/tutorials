from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "real estate properties"

    name = fields.Char('Property Name')
