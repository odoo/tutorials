from odoo import models, fields


class CommodityReq(models.Model):
    _name = 'commodity.req'
    _description = 'Commodity Requirements'

    name = fields.Char(string='Name', required=True)
