from odoo import  models
from datetime import timedelta
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def add_warranty_wizard_button(self):
        products = self.order_line
        for product in products:
            if product.product_template_id.is_warranty_available:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Add Warranty',
                    'res_model': 'add.warranty',
                    'view_mode': 'form',
                    'view_id': self.env.ref('warranty.view_warranty_form').id,
                    'target': 'new',  
                }
            else:
                raise UserError('This product does not have a warranty.')