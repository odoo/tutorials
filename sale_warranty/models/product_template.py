from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_warranty_available = fields.Boolean(
        string="Is Warranty Available?",
        default=False,
        help="Whether a warranty can be added to this product in the sales order."
    )
