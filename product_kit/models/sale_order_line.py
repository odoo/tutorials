from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit")
    parent_product_id = fields.Many2one('product.product')
    is_subproduct = fields.Boolean(default=False)

    def unlink(self):
        """
        Override unlink to also delete sub-product lines when a kit line is deleted.
        It also prevents the direct deletion of a sub-product line.
        """
        # Prevent direct deletion of sub-product lines.
        sub_product_lines = self.filtered('is_subproduct')
        if sub_product_lines:
            # Find the parent kit lines for these sub-products
            parent_lines = self.env['sale.order.line'].search([
                ('order_id', 'in', sub_product_lines.mapped('order_id').ids),
                ('product_id', 'in', sub_product_lines.mapped('parent_product_id').ids),
                ('is_kit', '=', True)
            ])
            # If any of the required parent lines are not in the current deletion set, raise an error.
            if parent_lines - self:
                raise UserError("You cannot delete a component of a kit directly. Please remove the main kit product instead.")

        # Cascade delete: find all sub-products of kits being deleted.
        sub_products_to_delete = self.env['sale.order.line']
        for line in self.filtered('is_kit'):
            sub_products_to_delete |= self.search([
                ('order_id', '=', line.order_id.id),
                ('parent_product_id', '=', line.product_id.id),
                ('is_subproduct', '=', True)
            ])

        all_records_to_delete = self | sub_products_to_delete
        return super(SaleOrderLine, all_records_to_delete).unlink()
