from odoo import models, fields


class SaleOrderLineDistributionTag(models.Model):
    _name = 'sale.order.line.distribution.tag'
    _description = 'Sale Order Line Distribution Tags'

    name = fields.Float(string="Distributed Amount")
