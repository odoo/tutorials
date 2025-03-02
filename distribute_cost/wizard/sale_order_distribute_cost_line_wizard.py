from odoo import api, models, fields

class SaleOrderDistributeCostLineWizard(models.TransientModel):
    _name = 'sale.order.distribute.cost.line.wizard'
    _description = 'Sale Order Cost Distribution Line Wizard'

    product_id = fields.Many2one('product.product', string="Product")
    allocated_price = fields.Float(string="Allocated Price")
    wizard_id = fields.Many2one("sale.order.distribute.cost.wizard", string="Cost Distribution Wizard", ondelete="cascade")
    sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', required=True)
    is_selected = fields.Boolean(default=True, string="Include in Cost Distribution")

    @api.onchange("is_selected")
    def _onchange_is_selected(self):
        if not self.is_selected:
            self.allocated_price = 0.0
        else:
            self.wizard_id._onchange_distribution_lines()
