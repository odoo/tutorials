from odoo import fields, models


class ProductWarrantyConfig(models.Model):
    _name = "product.warranty.config"
    _description = "Product Warranty Configuration"

    name = fields.Char(string="Name", required=True)
    product_template_id = fields.Many2one(
        "product.template", string="Product", required=True
    )
    percentage = fields.Float(string="Percentage", required=True)
    years = fields.Integer(string="Years", required=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Two Waranties can not be of same name"),
    ]
