# models/sale_order_line.py
from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    kit_parent_line_id = fields.Many2one('sale.order.line', string='Parent Kit Line', ondelete='cascade')
    is_kit_product = fields.Boolean(
        string="Is Kit Product", compute="_compute_is_kit", store=True
    )
    is_subproduct = fields.Boolean(string="Is Sub Product", default=False)

    @api.depends("product_id")
    def _compute_is_kit(self):
        for line in self:
            line.is_kit_product = line.product_id.product_tmpl_id.is_kit

    def write(self, vals):
        for line in self:
            if line.kit_parent_line_id:
                raise UserError("Sub product lines cannot be edited manually.")
        return super().write(vals)

    def open_kit_wizard(self):
        self.ensure_one()
        return {
            'name': f'Configure Kit: {self.product_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'kit.sub.product.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_line_id': self.id,
            }
        }

    @api.onchange('kit_parent_line_id')
    def _onchange_disable_edit(self):
        if self.kit_parent_line_id:
            self.update({'price_unit': 0})
