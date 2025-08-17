from odoo import api, fields, models


class SaleOrderDiscount(models.TransientModel):
    _inherit = "sale.order.discount"

    def update_discount(self):
        """
        Update the discount line based on current products in the order.
        
        Working :  extract the discount products order lines from the sale order line and unlink them
        create new discount product and add them to sales order line
        """
        order_id = self.env.context.get("active_id")
        if not order_id:
            return

        order = self.env["sale.order"].browse(order_id)
        discount_product = self.env.company.sale_discount_product_id
        if not discount_product:
            return

        discount_lines = order.order_line.filtered(lambda l: l.product_id == discount_product)
        non_discount_lines = order.order_line.filtered(lambda l: l.product_id != discount_product)

        if discount_lines:
            discount_lines.unlink()

        if non_discount_lines:
            latest_discount = order.global_discount
            wizard = self.env['sale.order.discount'].create({
                "sale_order_id": order.id,
                "discount_percentage": latest_discount,
                "discount_type": "so_discount",
            })
            wizard._create_discount_lines()

    def action_apply_discount(self):
        result = super().action_apply_discount()

        if self.discount_type != 'sol_discount':
            self.sale_order_id.global_discount = self.discount_percentage

        return result

