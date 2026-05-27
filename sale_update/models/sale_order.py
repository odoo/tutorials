from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_record_id = fields.Many2one("sale.order.discount.record")
