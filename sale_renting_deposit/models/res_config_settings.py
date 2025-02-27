from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_product_id = fields.Many2one(
        "product.product",
        string="Deposit",
        domain=[("type", "=", "service")],
        config_parameter="sale_renting.deposit_product_id",
    )
