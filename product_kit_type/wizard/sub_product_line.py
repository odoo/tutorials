from odoo import models, fields


class SubProductLineWizard(models.TransientModel):
    _name = "product_kit_type.subproducts.line"

    wizard_id = fields.Many2one("product_kit_type.subproducts", required=True)
    product_id = fields.Many2one("product.product", string="Product")
    product_qty = fields.Float(string="Quantity")
    price_unit = fields.Float(string="Price")
