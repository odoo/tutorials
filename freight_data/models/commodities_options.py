from odoo import fields, models


class CommoditiesOptions(models.Model):
    _name = "commodities.options"
    _description = "Freight Data Module"

    name = fields.Char()
