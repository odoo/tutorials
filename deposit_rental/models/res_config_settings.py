from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product_id = fields.Many2one("product.product", string="Deposite", config_parameter="sale_renting.deposit_product_id", domain=[("type", "=", "service")])

    def set_values(self):
        res = super().set_values()
        # Force recompute after changing the deposit product
        products = self.env["product.template"].search([("require_deposit", "=", True)])
        products._compute_deposit_amount()
        return res