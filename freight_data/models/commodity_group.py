from odoo import fields, models


class CommodityGroup(models.Model):
    _name = 'commodity.group'
    _description = 'Commodity Group Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
