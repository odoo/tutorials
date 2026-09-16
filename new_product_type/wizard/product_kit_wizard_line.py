from odoo import api, fields, models


class ProductKitWizardLine(models.TransientModel):
    _name = "product.wizard.kit.line"
    _description = "Kit Wizard Line"

    wizard_id = fields.Many2one('product.kit.wizard')
    product_id = fields.Many2one(
        'product.product',
        readonly=True
    )
    quantity = fields.Float(default=1.0)
    price = fields.Float()
    price_subtotal = fields.Float(
        string="Total Amount",
        compute="_check_total_price",
        store=True
    )

    @api.depends('quantity', 'price')
    def _check_total_price(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price
