from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    is_kit_visible = fields.Boolean(related="product_template_id.is_kit")
    kit_main_product_id = fields.Many2one("sale.order.line")

    def action_open_wizard(self):
        return {
            'type'      : 'ir.actions.act_window',
            'name'      : f'Product: {self.product_id.name}',
            'res_model' : 'product.sub.wizard',
            'view_type' : 'form',
            'view_mode' : 'form',
            'target'    : 'new',
            'context': {
                'product_template_id': self.product_template_id.id,
                'sale_order_line_id': self.id
            }
        }

    def unlink(self):
        for line in self:
            if not line.kit_main_product_id:
                self.search([('kit_main_product_id','=',line.id)]).filtered(lambda l: l not in self).unlink()
        return super(SaleOrderLine, self).unlink()
