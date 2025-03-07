from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_print_report = fields.Boolean(string="Print in Report", default=True)
