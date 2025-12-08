from odoo import fields, models


class ProductTypeKitWizardLine(models.TransientModel):
    _name = 'product.type.kit.wizard.line'
    _description = "Wizard Line for Kit Product Sub-Products"

    kit_product_wizard_id = fields.Many2one(comodel_name='product.type.kit.wizard', string="Wizard Reference")
    product_id = fields.Many2one(comodel_name='product.product', string="Product")
    quantity = fields.Float(string="Quantity", default=1.0)
    price = fields.Float(string="Price", default=0.0)
