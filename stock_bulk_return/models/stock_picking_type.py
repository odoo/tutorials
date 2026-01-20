# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        domain = ['|', ('display_name', operator, name), ('barcode', '=', name)]
        records = self.search_fetch(domain, ['display_name'], limit=limit)
        return [(record.id, record.display_name) for record in records.sudo()]
