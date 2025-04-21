# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ContainerisationSupplierWizard(models.TransientModel):
    _name = 'purchase.order.containerisation.supplier'
    _description = 'Wizard to select supplier that user wish to add lines from the PO transfers to a container.'

    supplier_id = fields.Many2one('res.partner', string='Supplier', domain="[('is_company', '=', True)]", required=True)

    def action_continue(self):
        picking_records = self.env['stock.picking'].search([
            ('partner_id', 'child_of', self.supplier_id.id),
            ('state', 'not in', ['done', 'cancel']),
            ('picking_type_id.code', '=', 'incoming'),
            ('is_container_picking', '=', False)
        ])
        move_lines = self.env['stock.move'].search([
            ('picking_id', 'in', picking_records.ids),
            ('product_uom_qty', '>', 0),
        ])
        action = self.env['ir.actions.act_window']._for_xml_id('purchase_order_containerisation.action_stock_move_container')
        action['domain'] = [('id', 'in', move_lines.ids)]
        action['context'] = {'default_line_ids': move_lines.ids, 'default_supplier_id': self.supplier_id.id}
        action['target'] = 'new'
        return action
