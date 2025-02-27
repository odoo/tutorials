from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    deposit_parent_product_id = fields.Many2one(
        comodel_name='product.product',
        string="Deposit for",
        help="Linked product line with deposit line."
    )
