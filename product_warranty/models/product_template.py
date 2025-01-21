from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_warranty = fields.Boolean(default=False, string="Warranty")
    warranty_configuration_ids = fields.One2many(
        "product.warranty.configuration", "product_template_id", string="Add Warranty"
    )
