from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_report = fields.Boolean(string="print in report?")