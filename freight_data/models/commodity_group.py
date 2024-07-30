from odoo import fields, models


class CommodityGroup(models.Model):
    _name = 'commodity.group'
    _description = 'Commodity Group Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')