# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    cont_type_id = fields.Many2one('stock.picking.type', string='Containerisation Operation Type')

    def _get_sequence_values(self, name=False, code=False):
        sequence_values = super()._get_sequence_values(name=name, code=code)
        sequence_values.update({
            'cont_type_id': {
                'name': _('%(name)s Sequence IN/CONT', name=self.name),
                'prefix': self.code + '/' + 'IN/CONT' + '/',
                'padding': 5,
                'company_id': self.company_id.id,
            }
        })
        return sequence_values

    def _get_picking_type_update_values(self):
        picking_type_update_values = super()._get_picking_type_update_values()
        picking_type_update_values.update({
            'cont_type_id': {
                'default_location_src_id': self.env.ref('stock.stock_location_suppliers').id,
                'barcode': self.code.replace(" ", "").upper() + "CONT"
            }
        })
        return picking_type_update_values

    def _get_picking_type_create_values(self, max_sequence):
        picking_type_create_values, max_sequence = super()._get_picking_type_create_values(max_sequence)
        picking_type_create_values.update({
            'cont_type_id': {
                'name': 'Containerisation',
                'code': 'incoming',
                'default_location_src_id': self.env.ref('stock.stock_location_suppliers').id,
                'default_location_dest_id': self.lot_stock_id.id,
                'sequence': max_sequence + 1,
                'sequence_code': 'IN/CONT',
                'company_id': self.company_id.id,
            }
        })
        return picking_type_create_values, max_sequence + 2
