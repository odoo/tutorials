from odoo import api, fields, models


class ResConfigSettingInherit(models.TransientModel):
    _inherit = "res.config.settings"

    rental_product_id = fields.Many2one(
        "product.product",
        string="Deposite Product",
        inverse="_set_rental_product",
        compute="_get_rental_product",
    )

    def _set_rental_product(self):
        self.env["ir.config_parameter"].set_param(
            "rental.deposite_product", self.rental_product_id.id or ""
        )

    @api.depends()
    def _get_rental_product(self):
        return int(self.env["ir.config_parameter"].get_param("rental.deposite_product"))
