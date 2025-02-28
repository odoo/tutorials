from odoo import fields, models

class SubProductLineWizard(models.TransientModel):
    _name = "sub.product.line.wizard"
    _description = "Sub Product Line Wizard"

    wizard_id = fields.Many2one('sub.product.wizard', ondelete="cascade")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    price = fields.Float(string="Price", required=True)
