from odoo import fields,models,_

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_add_warranty_wizard(self):
        
        available_products = self.order_line.filtered(
            lambda l: not l.related_product_id and l.product_id.product_tmpl_id.warranty and
                      not self.order_line.filtered(lambda w: w.related_product_id == l.product_id.product_tmpl_id)
        ).mapped("product_id.product_tmpl_id")

        product_warranty_data = []
        for product in available_products:
            related_line = self.order_line.filtered(lambda l: l.product_id.product_tmpl_id == product)
            quantity = sum(related_line.mapped("product_uom_qty")) if related_line else 1  # Default to 1 if not found

            product_warranty_data.append((0, 0, {
                'product_id': product.id,
                'year': False,
                'end_date': False,
                'quantity': quantity,
            }))

        return {
            'name': "Add Warranty",
            'type': 'ir.actions.act_window',
            'res_model': 'warranty.add.warranty',
            'view_mode': 'form',
            'target': 'new',
            'context': {
            'default_sale_order_id': self.id,   
            'default_product_warranty_ids': product_warranty_data,
        }
        }
