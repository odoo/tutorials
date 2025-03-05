from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(
        "Book Price", compute="_compute_book_price", default=0.0, store=True
    )

    @api.depends("product_id", "quantity", "move_id.invoice_line_ids")
    def _compute_book_price(self):
        for line in self:
            if not (line.product_id and line.move_id and line.move_id.invoice_line_ids):
                line.book_price = 0.0
                continue

            pricelist = (
                line.move_id.invoice_line_ids.sale_line_ids.order_id.pricelist_id
            )
            if pricelist:
                line.book_price = (
                    pricelist._get_product_price(
                        line.product_id, line.quantity, line.product_uom_id
                    )
                    if pricelist
                    else 0.0
                )
