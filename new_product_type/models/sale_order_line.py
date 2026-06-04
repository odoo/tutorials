from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit_line = fields.Boolean(related='product_id.product_tmpl_id.is_kit', store=True)
    is_kit_sub_line = fields.Boolean(default=False)
    kit_main_line_id = fields.Many2one('sale.order.line', string='Kit Main Line', ondelete='cascade')
    kit_unit_price = fields.Float(default=0.0)

    @api.ondelete(at_uninstall=False)
    def _check_sub_kit_product(self):
        for line in self:
            if line.is_kit_sub_line:
                raise UserError(
                    "You cannot delete a kit sub-product line directly. "
                    "Delete the main kit product line instead."
                )

    def action_open_kit_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Kit Sub Products',
            'res_model': 'sale.kit.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_line_id': self.id,
            },
        }
