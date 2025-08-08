# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    warranty_configuration_id = fields.Many2one(comodel_name='warranty.configuration')
    child_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line')

    @api.ondelete(at_uninstall=False)
    def _unlink_child_sale_order_line_id(self):
        for sale_order_line in self:
            if sale_order_line.child_sale_order_line_id:
                sale_order_line.child_sale_order_line_id.unlink()
