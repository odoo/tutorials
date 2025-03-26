from odoo import fields, models


class SaleOrderLineTag(models.Model):
    _name = 'sale.order.line.tag'

    name = fields.Char(string="Division Tag")
    color = fields.Integer(string="color", default='green')
