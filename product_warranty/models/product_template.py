from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_warranty = fields.Boolean(default=False, string="Is Warranty")
    warranty_ids = fields.One2many(
        "product.warranty",
        "product_template_id",
        string="Warranties"
    )
    