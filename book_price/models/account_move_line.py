from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        readonly=True,
        help="A relevant pricelist price based on currently selected pricelist, product and quantity.",
    )

    @api.depends("move_id.invoice_line_ids", "quantity", "product_id")
    def _compute_book_price(self):
        """Compute `book_price` based on the linked sale order's pricelist.
        - If a valid `product_id`, `move_id`, and `invoice_line_ids` exist:
          - Fetch the pricelist from the associated sale order.
          - Compute the price using `_get_product_price()` and multiply by quantity.
        - Otherwise, set `book_price` to 0.0."""
        
        for record in self:
            move = record.move_id
            record.book_price = 0.0
            if record.product_id and move and move.invoice_line_ids:
                product_pricelist = move.invoice_line_ids.mapped("sale_line_ids.order_id.pricelist_id")
                record.book_price = product_pricelist._get_product_price(record.product_id, record.quantity, record.product_uom_id) * record.quantity or 0.0

