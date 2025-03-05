from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_subproducts = fields.Boolean(string="Print in Report?")
