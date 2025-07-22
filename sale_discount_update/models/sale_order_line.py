# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_global_discount = fields.Boolean(
        string="Is Global Discount",
        default=False,
        help="Marks this line as a system-generated global discount"
    )
