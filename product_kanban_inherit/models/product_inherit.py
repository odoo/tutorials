from odoo import models, fields


class ProductInherit(models.Model):
    _inherit = "product.template"

    package_field = fields.Selection(
        [
            ("standard", "Standard"),
            ("bulk", "Bulk"),
            ("studio", "Studio"),
            ("custom", "Custom Packaging"),
        ],
        string="Package Type",
    )
