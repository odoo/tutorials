from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_kit = fields.Boolean(string="Print in report", default=True)
