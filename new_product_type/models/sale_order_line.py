from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit_available = fields.Boolean(related="product_template_id.is_kit")
    kit_component_ids = fields.One2many("sale.order.line", "parent_id")
    parent_id = fields.Many2one("sale.order.line", ondelete="cascade")
    
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
