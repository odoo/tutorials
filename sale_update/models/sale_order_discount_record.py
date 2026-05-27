from odoo import models, fields


class SaleOrderDiscountRecord(models.Model):
    _name = "sale.order.discount.record"

    order_id = fields.Many2one("sale.order")
    discount_percentage = fields.Float()
    discount_id = fields.Integer()
