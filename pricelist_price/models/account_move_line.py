from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(
        string="Book Price", 
        compute="_compute_book_price", 
        store=True,
    )

    @api.depends("product_id", "quantity", "sale_line_ids.order_id.pricelist_id")
    def _compute_book_price(self):
        """Compute the Book Price from the pricelist"""
        for line in self:
            if line.product_id:
                pricelist =  line.sale_line_ids.order_id.pricelist_id
                if pricelist:
                    line.book_price = pricelist._get_product_price(
                        line.product_id, line.quantity, line.product_uom_id
                    )
                else:
                    line.book_price = line.product_id.lst_price * line.quantity
            else:
                line.book_price = 0.0
