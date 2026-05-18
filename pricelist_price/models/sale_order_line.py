from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Float(compute="_compute_pricelist", readonly=True)

    @api.depends("product_id", "product_uom_qty", "order_id.pricelist_id", "product_template_id.list_price")
    def _compute_pricelist(self):
        for record in self:
            if not record.product_id:
                record.book_price = 0.0
            elif not record.order_id.pricelist_id:
                record.book_price = record.product_template_id.list_price
            else:
                record.book_price = record.order_id.pricelist_id._get_product_price(record.product_id, record.product_uom_qty)
