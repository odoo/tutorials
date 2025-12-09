from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    product_deposit = fields.Many2one('product.product', string="Product",
                                      domain=[("rent_ok", "=", True)])
