from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_marketplace_enabled = fields.Boolean(
        string="Enable Multi-Vendor Marketplace",
        config_parameter="website_sale.is_marketplace_enabled",
        default=False,
        help="Enable this option to allow multiple vendors to sell their products on your website. Each vendor will have their own shop and product listings, and customers can purchase from multiple vendors in a single order.",
    )

    def get_values(self):
        res = super().get_values()

        params = self.env["ir.config_parameter"].sudo()
        res.update(
            is_marketplace_enabled=params.get_param(
                "website_sale.is_marketplace_enabled", default=False
            )
        )

        return res

    def set_values(self):
        super().set_values()

        if self.is_marketplace_enabled:
            website = self.env["website"].sudo().search([])
            if website.auth_signup_uninvited != "b2c":
                website.sudo().write({"auth_signup_uninvited": "b2c"})
