from odoo import models, fields


class CommodityGroup(models.Model):
    _name = 'commodity.group'
    _description = 'Commodity Group'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
