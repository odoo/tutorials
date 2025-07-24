from odoo import fields, api, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_product = fields.Many2one("product.product", string="Deposit Product")

    def set_values(self):
        super().set_values()
        # Save the product ID or 0 if no product is selected
        self.env["ir.config_parameter"].sudo().set_param(
            "rental_deposit.deposit_product",
            self.deposit_product.id if self.deposit_product else 0,
        )

    @api.model
    def get_values(self):
        res = super().get_values()
        # Read the deposit product ID as string
        config_value = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("rental_deposit.deposit_product", default=0)
        )
        # Convert to int and browse the product; if empty or invalid, return empty recordset
        product = (
            self.env["product.product"].browse(int(config_value))
            if config_value
            else self.env["product.product"]
        )
        res.update(deposit_product=product)
        return res
