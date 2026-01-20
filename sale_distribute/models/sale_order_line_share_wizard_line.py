from odoo import api, fields, models


class SaleOrderLineShareWizardLine(models.TransientModel):
    _name = "sale.order.line.share.wizard.line"
    _description = "Sale Order Line Share Wizard Line"

    wizard_id = fields.Many2one("sale.order.line.share.wizard", string="Wizard")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    is_selected = fields.Boolean(string="Selected")
    amount = fields.Float(string="Amount")

    @api.onchange("is_selected", "wizard_id")
    def _onchange_is_selected(self):
        if not self.is_selected:
            self.amount = 0.0
