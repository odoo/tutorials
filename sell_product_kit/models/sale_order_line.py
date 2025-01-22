from odoo import _,fields, models

class InheritedProductTemplate(models.Model):
    _inherit= "sale.order.line"
    
    is_kit_product = fields.Boolean(
        string="Is the product is a kit?",
        related='product_template_id.is_kit',
        depends=['product_id']
    )
        
    def action_open_add_kit_wizard(self):
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Waning'),
                'type': 'warning',
                'message': "hello world",
                'sticky': False,
            }
        }
        return notification
    
