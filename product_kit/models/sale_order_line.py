from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit_product = fields.Boolean(related="product_template_id.is_kit")
    parent_line_id = fields.Many2one(comodel_name='sale.order.line', name="Linked kit product line", ondelete="cascade", domain="[('order_id', '=', order_id)]")

    @api.ondelete(at_uninstall=False)
    def _unlink_all_sub_product_lines(self):
        for line in self:
            if line.product_id.is_kit:
                linked_lines = self.env['sale.order.line'].filtered(lambda line: line.parent_line_id.id == self.parent_line_id.id)
                for linked_line in linked_lines:
                    linked_line.unlink()

    def action_open_kit_wizard(self):
        return {
            'name': f"Product: {self.product_id.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'sub.product.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
    
   