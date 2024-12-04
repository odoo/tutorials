from odoo import fields, models


class warranty(models.Model):
    _name = "warranty"
    _description = "warranty model for products"

    name = fields.Char(required=True)
    product_ids = fields.Many2one(comodel_name="product.product")
    percentage = fields.Float(DecimalPrecision=2)


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_warranty_available = fields.Boolean()


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def add_warranty_to_product(self):
        pass