from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_in_report = fields.Boolean(
        default=False, help="Print kits sub products in the report"
    )

    @api.onchange("order_line")
    def _onchange_order(self):
        current_kit_ids = {line._origin.id for line in self.order_line if line.product_is_kit}

        # filter out lines that are not kits and whose parent kit is not in the current kit ids (parent is_kit is deleted)
        new_order_lines = self.order_line.filtered(
            lambda line: not line.parent_kit_id.id
            or (line.parent_kit_id.id in current_kit_ids)
        )

        self.order_line = new_order_lines

    def _get_order_lines_to_report(self):
        order_lines = super()._get_order_lines_to_report()
        if self.print_in_report:
            return order_lines
        else:
            return order_lines.filtered(lambda line: line.product_is_kit)

    def _get_invoiceable_lines(self, final=False):
        invoicable_lines = super()._get_invoiceable_lines(final=final)
        if self.print_in_report:
            return invoicable_lines
        else:
            return invoicable_lines.filtered(lambda line: line.product_is_kit)
