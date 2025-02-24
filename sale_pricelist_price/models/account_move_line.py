from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string="Book Price", compute="_compute_book_price")

    @api.depends("product_id", "quantity", "move_id.invoice_line_ids")
    def _compute_book_price(self):
        for line in self:
            pricelist = line.move_id.invoice_line_ids.sale_line_ids.order_id.pricelist_id
            if pricelist:
                line.book_price = pricelist._get_product_price(line.product_id, line.quantity, line.product_uom_id)
            else:
                line.book_price = line.product_id.list_price
