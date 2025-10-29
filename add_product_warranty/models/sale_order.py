from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_warranty_button = fields.Boolean(
        string="Show Warranty Button",
        compute="_compute_show_warranty_button",
        store=True
    )

    @api.depends("order_line")
    def _compute_show_warranty_button(self):
        for order in self:
            show_button = False
            for line in order.order_line:
                # Check if this product has warranty available
                if line.product_template_id.is_warranty_available:
                    # And there is no other line that links to this line as warranty
                    linked_as_warranty = any(
                        l.warranty_line_linked_with_so_line == line
                        for l in order.order_line
                    )
                    if not linked_as_warranty:
                        show_button = True
                        break  # We can stop early if condition is satisfied

            order.show_warranty_button = show_button

    @api.onchange("order_line")
    def _onchange_order_line(self):
        original_line_ids = self._origin.order_line.ids

        current_line_ids = self.order_line.ids

        deleted_line_ids = list(set(original_line_ids) - set(current_line_ids))

        if deleted_line_ids:
            # Remove warranty lines linked to deleted lines
            self.order_line = [
                (
                    6,
                    0,
                    self.order_line.filtered(
                        lambda line: line.warranty_line_linked_with_so_line.id
                        not in deleted_line_ids
                    ).ids,
                )
            ]
