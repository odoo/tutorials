from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_related_product = fields.Boolean(
        string="Is Related Product",
        default=False,
        help="Indicates if this product was automatically added as a related product."
    )
