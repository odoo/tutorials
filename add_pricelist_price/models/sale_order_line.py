from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    book_price = fields.Monetary(
        string="Book Price",
        compute="_compute_book_price",
        store=True,
        readonly=True,
        help="The original price fetched from the pricelist rule before any manual overrides."
    )

    @api.depends("product_id", "product_uom_qty", "order_id.pricelist_id")
    def _compute_book_price(self):
        for line in self:
            if not line.product_id:
                line.book_price = 0.0
                continue

            pricelist = line.order_id.pricelist_id

            if pricelist:
                unit_price = pricelist._get_product_price(line.product_id, line.product_uom_qty)
            else:
                unit_price = line.product_id.lst_price or 0.0

            line.book_price = unit_price
