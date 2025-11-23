# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def open_warranty_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'warranty.wizard',
            'views': [(False, 'form')],
            'target': 'new'
        }
