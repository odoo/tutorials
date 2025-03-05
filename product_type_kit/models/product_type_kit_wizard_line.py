from odoo import fields, models


class ProductTypeKitWizardLine(models.TransientModel):
    _name = 'product.type.kit.wizard.line'
    _description = "Wizard Line for Sub Products"

    wizard_id = fields.Many2one(
        comodel_name='product.type.kit.wizard',
        string="Wizard",
        required=True,
        ondelete='cascade')
    product_id = fields.Many2one(comodel_name='product.product', string="Product")
    quantity = fields.Float(string="Quantity", default=1)
    price = fields.Float(string="Price")
