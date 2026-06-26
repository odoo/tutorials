from odoo import api, fields, models


class KitConfigWizardLine(models.TransientModel):
    _name = 'kit.config.wizard.line'
    _description = 'Kit Configuration Wizard Line'

    wizard_id = fields.Many2one(
        'kit.config.wizard',
        string="Wizard",
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product',
        string="Product",
        required=True,
    )
    quantity = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
    )
    price_unit = fields.Float(
        string="Unit Price",
        required=True,
    )
    subtotal = fields.Float(
        string="Subtotal",
        compute='_compute_subtotal',
        store=True,
    )

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
