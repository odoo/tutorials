# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_warranty_product = fields.Boolean(
        string="Has Warranty Product", store=True,
        compute='_compute_has_warranty_product'
    )

    @api.depends('order_line.product_id')
    def _compute_has_warranty_product(self):
        for order in self:
            order.has_warranty_product = any(line.product_id.warranty for line in order.order_line)

    def open_add_warranty_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Warranty Products',
            'res_model': 'product.warranty.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_id': self.id}
        }
