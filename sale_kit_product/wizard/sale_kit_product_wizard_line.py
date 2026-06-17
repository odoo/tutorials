from odoo import fields, models


class SaleKitProductWizardLine(models.TransientModel):
    _name = "sale.kit.product.wizard.line"
    _description = "This is the model for showing the sub product lines in wizard."

    product_wizard_line = fields.Many2one("sale.kit.product.sub.product.wizard")
    product_id = fields.Many2one("product.product")
    product_qty = fields.Integer(default=0, string="Quantity")
    product_price = fields.Float(string="Unit Price ")
