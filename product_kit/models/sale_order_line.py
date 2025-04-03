from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit", store=True)
    from_wizard = fields.Boolean(string="Created from Wizard", default=False)


    def action_open_kit_wizard(self):
        """Opens the wizard with Sale Order ID in context"""
        return {
            "name": "Kit Products",
            "type": "ir.actions.act_window",
            "res_model": "kit.products.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_sale_order_id": self.order_id.id,  
                "default_product_template_id": self.product_template_id.id,
            }
        }
