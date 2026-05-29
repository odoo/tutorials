from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_marketplace_enabled = fields.Boolean(
        string="Enable Multi-Vendor Marketplace",
        config_parameter="web_sale.is_marketplace_enabled",
        default=False,
        help="Enable this option to allow multiple vendors to sell their products on your website. Each vendor will have their own shop and product listings, and customers can purchase from multiple vendors in a single order.",
    )