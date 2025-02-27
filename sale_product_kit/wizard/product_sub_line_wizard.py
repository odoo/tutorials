from odoo import fields, models

class ProductSubWizardLine(models.TransientModel):
    _name = "product.sub.wizard.line"
    _description = "Sub Product Line"

    wizard_id = fields.Many2one("product.sub.wizard", string="Wizard")
    product_id = fields.Many2one("product.product", string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    price = fields.Float(string="Price", required=True)
