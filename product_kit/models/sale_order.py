from odoo import api,models,fields


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    print_in_report = fields.Boolean(default=False)
