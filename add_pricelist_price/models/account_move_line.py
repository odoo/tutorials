from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Float(string="Book Price", compute="_compute_book_price", store=True)

    @api.depends('product_id', 'quantity', 'move_id.invoice_line_ids')
    def _compute_book_price(self):
        for line in self:
            if not line.product_id:
                line.book_price = (line.product_id.lst_price * line.quantity)
                continue

            if line.move_id.invoice_line_ids:
                pricelist = line.move_id.invoice_line_ids.sale_line_ids.order_id.pricelist_id

            if not pricelist:
                # Fallback to the partner's pricelist if no sale order pricelist is found
                pricelist = line.move_id.partner_id.property_product_pricelist

            if pricelist:
                line.book_price = pricelist._get_product_price(
                    line.product_id,
                    line.quantity,
                    line.product_uom_id,
                )
                line.book_price = (line.book_price * line.quantity)
