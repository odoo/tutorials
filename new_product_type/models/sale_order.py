from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_report = fields.Boolean(
        string="Print Kit Sub-Products in Report",
        default=False,
        help="Enable this to display kit sub-products in the sales report and invoice."
    )
