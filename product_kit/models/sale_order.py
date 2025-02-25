from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_in_report = fields.Boolean(string='Print in report?', help='allow sub products to print')
