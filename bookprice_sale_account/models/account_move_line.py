from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # computational field for book price    
    book_price = fields.Float(
        string="Book Price",
        compute="_compute_book_price",
        help="Price without any discount and taxes",
    )

    @api.depends('product_id', 'quantity', 'move_id.partner_id.property_product_pricelist')
    def _compute_book_price(self):
        for line in self:
            if line.move_type != 'out_invoice':
                line.book_price = 0.0
                continue
            # if invoice have single sale order line then use the book price using sale_line_ids
            if len(line.sale_line_ids) == 1:
                line.book_price = line.sale_line_ids.book_price
                continue
            pricelist = (
                len(line.sale_line_ids.order_id) == 1
                and line.sale_line_ids.order_id.pricelist_id
                or line.partner_id.specific_property_product_pricelist
            )
            if pricelist:
                line.book_price = line.sale_line_ids.order_id.pricelist_id._get_product_price(
                    line.product_id,
                    line.quantity,
                    line.product_uom_id
                )
            else:
                line.book_price = line.product_id.lst_price
