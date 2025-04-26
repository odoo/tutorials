from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"


    def open_warranty_wizard(self):

        return {
        'type': 'ir.actions.act_window',
        'name': 'Add Warranty',
        'res_model': 'add.warranty.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {'default_sale_order_id': self.id},
        }

