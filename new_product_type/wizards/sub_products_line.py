from odoo import api, fields, models


class SubProductsLineWizard(models.TransientModel):
    _name = "sub.products.line.wizard"

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        help="The product for which sub-products are being selected",
    )
    quantity = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
        help="The quantity of the sub-product to be added",
    )
    price = fields.Float(
        string="Price", required=True, help="The price of the sub-product"
    )
    sub_products_wizard_id = fields.Many2one(
        "sub.products.wizard",
        string="Sub Products Wizard",
        required=True,
        ondelete="cascade",
        help="The wizard from which this line is being created",
    )
