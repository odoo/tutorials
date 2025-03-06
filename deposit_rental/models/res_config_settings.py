from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_product_id = fields.Many2one(
        "product.product",
        string="Deposit Product",
        related="company_id.deposit_product_id",  
        readonly=False
    )
