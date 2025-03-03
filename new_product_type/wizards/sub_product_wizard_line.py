from odoo import fields, models


class SubProductWizardLine(models.TransientModel):
    _name = "sub.product.wizard.line"
    _description = "Wizard Line for Kit Products"

    wizard_id = fields.Many2one("sub.product.wizard", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    price = fields.Float(default=0.0)
