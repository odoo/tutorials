from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(
        related='product_template_id.is_kit',
        depends=['product_id']
    )

    parent_line_id = fields.Many2one('sale.order.line', string="Parent Line", ondelete='cascade')

    def action_open_kit_wizard(self):
        return {
            'name': f"Product: {self.product_id.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'sub.product.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
    

    
