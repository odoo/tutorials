# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, _, api, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_warranty_wizard(self):
        view_id = self.env.ref('warranty.view_warranty_wizard_form').id
        name = _('Warranty Configuration')
        sale_order_line_ids = self.order_line.filtered(lambda line: line.product_template_id.is_warranty_available).ids
        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'res_model': 'warranty.wizard',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_sale_order_line_ids': sale_order_line_ids,
                'default_sale_order_id': self.id,
            },
        }
