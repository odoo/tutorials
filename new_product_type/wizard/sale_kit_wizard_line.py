from odoo import models, fields


class SaleKitWizardLine(models.TransientModel):
    _name = 'sale.kit.wizard.line'
    _description = 'Sale Kit Wizard Line'

    wizard_id = fields.Many2one('sale.kit.wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(default=1.0, digits=(16, 2))
    price = fields.Float(digits=(16, 2))
