from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _only_discount_lines_exist(self, order):
        """
        Check if only discount product lines exist in the order.

        return : True when only discount product present
        """
        discount_product = self.env.company.sale_discount_product_id
        return bool(order and discount_product and all(line.product_id == discount_product for line in order.order_line))

    def _remove_discount_lines(self,order):
        """Remove all discount order lines."""
        discount_lines = self.filtered(lambda l: l.product_id == self.env.company.sale_discount_product_id)
        if discount_lines:
            discount_lines.unlink()
        order.global_discount = 0.0

    def _trigger_discount_update(self, order):
        if order:
            self.env["sale.order.discount"].with_context(active_id=order.id).update_discount()

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to update discount when new products are added."""
        discount_product = self.env.company.sale_discount_product_id

        creating_discount_product = any(vals.get('product_id') == discount_product.id for vals in vals_list)

        lines = super().create(vals_list)
        order = lines[0].order_id  

        if not creating_discount_product:
            if(order.global_discount != 0.0):
                lines[0]._trigger_discount_update(order)

        return lines

    def unlink(self):
        """Override unlink to update discount when products are removed."""
        order = self.mapped("order_id")
        if not order:
            return super().unlink()

        removing_discount_product = bool(self.filtered(lambda l: l.product_id == self.env.company.sale_discount_product_id))

        line_removed = super().unlink()

        if not removing_discount_product:
            if self._only_discount_lines_exist(order):
                order.order_line._remove_discount_lines(order)
            else:
                self._trigger_discount_update(order)

        return line_removed
