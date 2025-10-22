from odoo import fields, models


class ProductCatalogInherited(models.Model):
    _inherit = "product.template"

    package_field = fields.Selection(
        [
            ("carton", "Carton"),
            ("bulk", "Bulk"),
            ("studio", "Studio"),
        ],
        string="Package Field",
    )
