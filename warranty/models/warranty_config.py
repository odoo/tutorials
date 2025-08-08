from odoo import _, fields, models


class WarrantyConfig(models.Model):
    _name = "warranty.config"
    _description = "Warranty Configuration"

    _sql_constraints = [
        ('unique_product_year', 'UNIQUE(product_id, year)', 'A warranty configuration already exists for this product and year combination.'),
        ('check_year_positive', 'CHECK(year > 0)', 'Warranty Period must be Positive.')
    ]

    name = fields.Char("Name", required=True)
    product_id = fields.Many2one("product.template", string="Product", required=True)
    percentage = fields.Float("Percentage", required=True)
    year = fields.Integer("Year", required=True, default=1)
