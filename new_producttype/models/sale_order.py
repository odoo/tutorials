from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_report = fields.Boolean(string="Print in Report")
