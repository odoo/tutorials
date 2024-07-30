from odoo import fields, models


class CommodityRequest(models.Model):
    _name = 'commodity.request'
    _description = 'Commodity Request Selection Options'

    name = fields.Char(required=True, string="Coomodity Request")
