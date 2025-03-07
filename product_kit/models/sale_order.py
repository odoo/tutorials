from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_printable = fields.Boolean(string="Print in Report ?")
