from odoo import models, fields


class SubProductWizardLine(models.TransientModel):
    _name = "sale.sub.product.wizard.line"

    product_id = fields.Many2one("product.product", string="Product")
    quantity = fields.Float(default=1.0, required=True)
    price = fields.Float(default=0.0, required=True)
    sub_product_wizard_id = fields.Many2one(comodel_name="sale.sub.product.wizard")
