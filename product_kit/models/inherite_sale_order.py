from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    include_sub_products_in_report = fields.Boolean(string="Print in Report?", default=False)
