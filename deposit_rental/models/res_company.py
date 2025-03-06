from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    deposit_product_id = fields.Many2one(
        "product.product",
        string="Deposit Product",
    )
    