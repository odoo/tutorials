# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    quantity_to_containerise = fields.Float(string='Quantity to Containerisation')

    def action_continue_container(self):
        supplier_id = self.env.context.get('default_supplier_id')
        active_ids = self.ids
        action = self.env['ir.actions.act_window']._for_xml_id('purchase_order_containerisation.action_containerisation_wizard')
        action['context'] = {'default_active_ids': active_ids, 'default_supplier_id': supplier_id}
        action['target'] = 'new'
        return action
