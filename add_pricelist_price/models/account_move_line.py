from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Monetary(
        string="Book Price",
        compute="_compute_book_price",
        readonly=True,
    )

    @api.depends('product_id', 'quantity', 'move_id.partner_id')
    def _compute_book_price(self):
        for line in self:
            if not line.product_id:
                line.book_price = 0.0
                continue

            if line.sale_line_ids:
                pricelist = line.sale_line_ids[0].order_id.pricelist_id
            else:
                pricelist = line.move_id.partner_id.property_product_pricelist

            if pricelist:
                line.book_price = pricelist._get_product_price(
                    product=line.product_id,
                    quantity=line.quantity,
                )
            else:
                line.book_price = line.product_id.list_price
