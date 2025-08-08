from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_kit_printable = fields.Boolean(string="Print in report ?", default=True)
