from odoo import api, models


class SalesOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('order_line')
    def _onchange_delete_warranty(self):
        for line in self.order_line:

            if line.warranty_product_id:
                flag = True

                for record in self.order_line:

                    line_id = str(record.id)
                    line_id = line_id.split('_')

                    if len(line_id) > 2:
                        continue

                    line_id = int(line_id[-1])

                    if int(line_id) == line.warranty_product_id:
                        flag = False

                if flag:
                    self.order_line -= line
