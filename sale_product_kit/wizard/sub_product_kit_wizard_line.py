from odoo import fields, models


class SubProductKitWizardLine(models.TransientModel):
    _name = "sub.product.kit.wizard.line"
    _description = "Wizard Sub Products"

    wizard_id = fields.Many2one("sub.product.kit.wizard", string="wizard")
    product_id = fields.Many2one("product.product", string="Product")
    quantity = fields.Float(string="Quantity", default=1.0)
    price = fields.Float(string="Price")
    existing_line_id = fields.Many2one("sale.order.line")
