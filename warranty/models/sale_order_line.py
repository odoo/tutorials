from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_end_date = fields.Date("Warranty End Date")
