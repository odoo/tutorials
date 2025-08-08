from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    show_on_global_info = fields.Boolean(
        string="Show on Global info",
        help="If checked, this category will appear in the 'Global Info' tab of Sale Orders.",
        default=False,
        store=True
    )

    required_attribute_ids = fields.Many2many(
        comodel_name="product.attribute",
        string="Required Attribute",
        help="Attributes that must be specified for products in this category."
    )
