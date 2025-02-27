from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Float(string="Book Price", compute='_compute_book_price', store=True)

    @api.depends('product_id', 'quantity', 'move_id.invoice_origin')
    def _compute_book_price(self):
        for line in self:
            if not line.product_id:
                line.book_price = 0.0
                continue

            line.book_price = line.product_id.lst_price * line.quantity

            sale_order = self.env['sale.order'].search(
                [("name", "=", line.move_id.invoice_origin)], limit=1
            )

            pricelist = sale_order.pricelist_id if sale_order else None

            if not pricelist:
                # Fallback to the partner's pricelist if no sale order pricelist is found
                pricelist = line.move_id.partner_id.property_product_pricelist

            if pricelist:
                line.book_price = pricelist._get_product_price(
                    line.product_id,
                    line.quantity,
                    line.product_uom_id,
                )
                line.book_price = line.book_price * line.quantity
