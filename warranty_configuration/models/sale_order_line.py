from odoo import models,api,fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line" 
    
    @api.model_create_multi
    def create(self, vals_list):
        print(vals_list)
        return []
    
    def action_add_warranty(self):
        print("-*- " * 100)
        print("hello from warranty !")
        print("-*- " * 100)
        
        return []
