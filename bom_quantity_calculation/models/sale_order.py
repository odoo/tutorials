from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    order_of_work = fields.Char(string="Order of Work")
