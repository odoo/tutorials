# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(related='product_id.is_kit')
    price_sub_product = fields.Monetary(string="Unit price of sub-product")

    kit_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string="Linked kit product line",
        ondelete='cascade',
        domain="[('order_id', '=', order_id)]",
    )
    sub_line_ids = fields.One2many(comodel_name='sale.order.line', inverse_name='kit_line_id', string="Linked sub-product lines")

    @api.depends('is_kit', 'kit_line_id')
    def _compute_product_updatable(self):
        super()._compute_product_updatable()
        self.filtered(lambda line: line.is_kit or line.kit_line_id).write({'product_updatable': False})

    @api.depends('kit_line_id')
    def _compute_product_uom_readonly(self):
        super()._compute_product_uom_readonly()
        self.filtered(lambda line: line.kit_line_id).write({'product_uom_readonly': True})

    def action_edit_sub_products(self):
        self.ensure_one()
        return {
            'name': _("Product: %s", self.product_id.name),
            'type': 'ir.actions.act_window',
            'res_model': 'edit.sub.product',
            'view_mode': 'form',
            'target': 'new',
        }
