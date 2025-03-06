from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit = fields.Many2one(
        "product.product",
        string="Deposit",
        related="company_id.deposit",
        readonly=False,
    )
