from odoo import models, api, Command

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _onchange_order_line(self):
        super()._onchange_order_line()
        deleted_product_ids = []
        for line in self.order_line:
            # Find each products that is not in SO currently
            if line.linked_line_id.id and line.linked_line_id.id not in self.order_line.ids:
                deleted_product_ids.append(line.linked_line_id.id)
        #  delete the warranty also for that deleted product. 
        #  each warranty have its corresponsding product id in linked_line_id
        linked_line_ids_to_delete = self.order_line.search([('linked_line_id', 'in', deleted_product_ids)])
        self.order_line = [Command.delete(linked_line_id) for linked_line_id in linked_line_ids_to_delete.ids]
