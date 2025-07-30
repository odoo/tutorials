from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_subproducts = fields.Boolean(string="Print in report?", default=True)
