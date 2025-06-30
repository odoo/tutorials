from odoo import models, fields


class EcommerceProductCategory(models.Model):
    _name = "ecommerce.product.category"
    _description = "E-commerce Product Category"

    name = fields.Char(string="Category Name", required=True)
    description = fields.Text(string="Description")
    product_id = fields.Many2one(
        comodel_name="ecommerce.product",
        string="Product Category",
        ondelete="cascade",
    )
    