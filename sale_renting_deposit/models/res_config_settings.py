from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_product_id = fields.Many2one(
        "product.product",
        string="Deposit Product",
        domain=[("deposit_product", "=", "True")],
        config_parameter="sale_renting.deposit_product_id"
    )

    def set_values(self):
        super().set_values()
        self.env["ir.config_parameter"].set_param("rental.deposit_product_id", self.deposit_product_id.id if self.deposit_product_id else False)

    @api.model
    def get_values(self):
        res = super().get_values()
        deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("rental.deposit_product_id", default=False)
        res.update({
            'deposit_product_id': int(deposit_product_id) if deposit_product_id else False
        })
        return res

