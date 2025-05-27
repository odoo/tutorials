from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string="Book Price", compute="_compute_book_price")

    @api.depends("product_id", "quantity", "sale_line_ids.order_id.pricelist_id")
    def _compute_book_price(self):
        for line in self:
            sale_order = line.sale_line_ids.order_id
            pricelist = sale_order.pricelist_id if sale_order else None
            if pricelist:
                line.book_price = pricelist._get_product_price(
                    line.product_id,
                    line.quantity,
                    line.product_uom_id,
                )
            else:
                line.book_price = line.product_id.lst_price
