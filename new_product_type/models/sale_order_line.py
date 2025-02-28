from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit= "sale.order.line"
    
    is_kit = fields.Boolean()    

    def action_open_add_kit_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sub Product',
            'res_model': 'sub.product.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
