# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    product_min_qty = fields.Float(string="Minimum Quantity")

    _sql_constraints = [
        ("product_min_qty", "CHECK(product_qty >= product_min_qty)", "Quantity cannot be lower than Minimum Quantity")
    ]
