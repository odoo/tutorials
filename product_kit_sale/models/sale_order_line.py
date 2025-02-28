# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    show_kit_button = fields.Boolean(compute="_compute_kit_button")
    parent_kit_line_id = fields.Many2one(comodel_name="sale.order.line", ondelete="cascade")
    sub_product_line_ids = fields.One2many(comodel_name="sale.order.line", inverse_name="parent_kit_line_id")
    sub_product_effective_price = fields.Float(help="Product price shown in wizard")

    @api.depends("product_id", "order_id.state")
    def _compute_kit_button(self):
        for line in self:
            line.show_kit_button = line.product_id.is_kit and line.order_id.state == 'draft'

    def action_open_kit_wizard(self):
        self.ensure_one()
        return {
            'name': f"Product: {self.product_id.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.kit',
            'view_mode': 'form',
            'target': 'new',
        }
