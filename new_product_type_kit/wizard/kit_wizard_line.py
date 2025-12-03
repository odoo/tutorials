from odoo import fields, models


class KitWizardLine(models.TransientModel):
    _name = 'kit.wizard.line'
    _description = 'Kit Wizard Line'

    wizard_id = fields.Many2one('kit.wizard', string="Wizard", required=True, ondelete="cascade")
    product_id = fields.Many2one('product.product', string="Sub Product")
    quantity = fields.Float(string="Quantity", default=1.0, required=True)
    price = fields.Float(string="Price")
