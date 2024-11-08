from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_print_sub_products = fields.Boolean(string="Print in report?")
