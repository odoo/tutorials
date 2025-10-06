from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    global_discount = fields.Float("Global Discount")
