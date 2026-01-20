from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string="Book Price", compute="_compute_book_price")

    @api.depends('product_id', 'quantity', 'product_uom_id', 'sale_line_ids.order_id.pricelist_id')
    def _compute_book_price(self):
        for line in self:
            line.book_price = 0.0
            if not line.product_id:
                continue

            sale_line = line.sale_line_ids[:1]
            if sale_line:
                pricelist = sale_line.order_id.pricelist_id
                if pricelist:
                    line.book_price = pricelist._get_product_price(
                        line.product_id, line.quantity, line.product_uom_id
                    )
                    continue
            line.book_price = line.product_id.lst_price
