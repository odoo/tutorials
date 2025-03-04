# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    global_discount_percentage = fields.Float(
        string="Global Discount (%)",
        help="Stores the global discount percentage applied to the sale order.",
        default=0.0
    )
