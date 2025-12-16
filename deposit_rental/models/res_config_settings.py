from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product = fields.Many2one(
        "product.product",
        related="company_id.deposit_product",
        string="Deposit",
        readonly=False
    )
