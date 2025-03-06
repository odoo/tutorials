from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = ["purchase.order"]

    order_of_work = fields.Char(string="Order of Work")
