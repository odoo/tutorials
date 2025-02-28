from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit_available = fields.Boolean(related="product_template_id.is_kit")

    def action_open_wizard(self):
        self.ensure_one()
        return {
            'name': 'Add Sub Product',
            'type': 'ir.actions.act_window',
            'res_model': 'sub.product.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id}
        }
