from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Float(string="Book Price", readonly=True, compute="_compute_book_price")  # Remove compute

    @api.depends('product_id', 'product_uom_id')
    def _compute_book_price(self):

        for record in self:
            move = record.move_id
            record.book_price = 0.0
            if record.product_id and move and move.invoice_line_ids:
                product_pricelist = move.invoice_line_ids.mapped("sale_line_ids.order_id.pricelist_id")
                record.book_price = product_pricelist._get_product_price(record.product_id, record.quantity, record.product_uom_id) * record.quantity or 0.0
