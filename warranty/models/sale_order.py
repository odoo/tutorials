from odoo import fields,models,_

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_add_warranty_wizard(self):
        return {
            'name': "Add Warranty",
            'type': 'ir.actions.act_window',
            'res_model': 'warranty.add.warranty',
            'view_mode': 'form',
            'target': 'new',
            'context': {
            'default_sale_order_id': self.id,   
        }
        }
