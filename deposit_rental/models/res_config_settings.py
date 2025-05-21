from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_product_id = fields.Many2one(
        "product.product",
        string="Deposite",
        config_parameter="sale_renting.deposit_product_id",
        domain=[("type", "=", "service")],
        help="Product used as a deposit when renting."
    )

    def set_values(self):
        old_deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("sale_renting.deposit_product_id")
        super().set_values()
        new_deposit_product_id = self.deposit_product_id.id or False

        if old_deposit_product_id != new_deposit_product_id:
            products = self.env["product.template"].search([
                ("require_deposit", "=", True)
            ])
            products._compute_deposit_amount()
