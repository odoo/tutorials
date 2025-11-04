from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    sub_products_in_report = fields.Boolean(string="Print in Report?")
