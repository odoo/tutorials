from odoo import models, fields


class KitProductsWizardLine(models.TransientModel):
    _name = "kit.products.wizard.line"
    _description = "Kit Products Wizard Line"

    wizard_id = fields.Many2one("kit.products.wizard", required=True)
    product_id = fields.Many2one("product.product", string="Product")
    product_qty = fields.Float(string="Quantity")
    price_unit = fields.Float(string="Price")
