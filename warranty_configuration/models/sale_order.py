from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"
        
    def action_open_warranty_wizard(self):
        print("-" * 100)
        # Properly define the return dictionary for the wizard action
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Warranty',
            'res_model': 'warranty.configuration',  # Your wizard model
            'view_mode': 'form',
            'view_id': self.env.ref('warranty_configuration.view_add_warranty_wizard').id,  # Adjust the module/view XML ID
            'target': 'new',
            'context': {
                'default_product_ids': self.order_line.ids,  # Adjust based on the wizard's logic
            },
        }
