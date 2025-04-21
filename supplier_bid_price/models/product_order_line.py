from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    bid_qty = fields.Float(string="Bid Quantity")
    bid_price = fields.Float(string="Bid Price")
