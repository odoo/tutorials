from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    subproduct_print = fields.Boolean()
