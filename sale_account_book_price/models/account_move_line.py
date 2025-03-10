from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Float(
        string="Book Price",
        compute='_compute_book_price',
        help="Computes the book price form product_id, move_id.partner_id, quantity"
    )

    @api.depends('product_id', 'move_id.partner_id', 'quantity')
    def _compute_book_price(self):
        for line in self:
            if line.move_id.move_type != 'out_invoice':
                line.book_price = 0.0
                continue

            if len(line.sale_line_ids) == 1:
                line.book_price = line.sale_line_ids.book_price

            elif len(line.sale_line_ids.order_id.pricelist_id) == 1:
                pricelist = line.sale_line_ids.order_id.pricelist_id
                line.book_price = pricelist._get_product_price(
                    line.product_id,
                    line.quantity,
                    line.move_id.partner_id
                )

            elif line.move_id.partner_id.property_product_pricelist:
                pricelist = line.move_id.partner_id.property_product_pricelist
                line.book_price = pricelist._get_product_price(
                    line.product_id,
                    line.quantity,
                    line.move_id.partner_id
                )

            else:
                line.book_price = line.product_id.lst_price
