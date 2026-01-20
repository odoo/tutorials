from odoo import fields, models


class ProductKitWizardLine(models.TransientModel):
    _name = 'product.kit.wizard.line'
    _description = 'Key-Value Line for Product Kit Wizard'

    wizard_id = fields.Many2one(
        'product.kit.wizard', string='Wizard', ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.product', string='Product', required=True, ondelete='cascade'
    )
    quantity = fields.Float(string='Quantity', required=True)
    price = fields.Float(string='Price', required=True)
