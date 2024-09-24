from odoo import api, models


class SalesOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('order_line')
    def _delete_warranty_onchange(self):
        print("on change")
        # self.order_line.unlink
        product_list = []
        for line in self.order_line:
            product_list.append(line.product_template_id.id)
        
        product =set(product_list)
        print(product)

        # warranty_list = []
        # for line in self.order_line:
        #     print(f"{line.name}, {line.product_template_id.warranty_available}, id- {line.id}, parent_id- {line.warranty_product_id}")
        #     print(f"-->name {line.product_template_id.name}, id- {line.product_template_id.id}")
            
        #     if line.warranty_product_id:
        #         warranty_list.append(line.warranty_product_id)
        #     else:
        #         product_list.append(line.product_template_id.id)
        # print(warranty_list)
        # print(product_list)

        # # Assuming product_list is a list, we convert it to a set for faster lookups
        # product_set = set(product_list)

        # for line in self.order_line:
        #     if line.warranty_product_id and line.warranty_product_id not in product_set:
        #         line.unlink()
                # parent = self.env['sale.order.line'].browse(line.warranty_product_id)
                # parent.unlink()
        

    
    @api.ondelete(at_uninstall=False)
    def _delete_order_line_product(self):

        print("deletion called")