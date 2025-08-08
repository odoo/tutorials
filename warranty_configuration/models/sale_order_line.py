# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    child_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line')
    warranty_configuration_id = fields.Many2one(comodel_name='warranty.configuration')

    @api.ondelete(at_uninstall=False)
    def _unlink_child_sale_order_line_id(self):
        for sale_order_line in self:
            if sale_order_line.child_sale_order_line_id:
                sale_order_line.child_sale_order_line_id.unlink()

    @api.depends('child_sale_order_line_id')
    def _compute_product_updatable(self):
        super()._compute_product_updatable()
        warranty_product_ids = set(self.env['warranty.configuration'].search([]).mapped('product_id'))
        for sale_order_line in self:
            sale_order_line.product_updatable = not (sale_order_line.child_sale_order_line_id or (sale_order_line.product_id in warranty_product_ids))

    @api.onchange('product_uom_qty', 'price_unit')
    def _onchange_sale_order_line(self):
        child_line = self.child_sale_order_line_id
        if child_line:
            child_line.product_uom_qty = self.product_uom_qty
            child_line.price_unit = self.price_unit * (self.warranty_configuration_id.percentage / 100)
