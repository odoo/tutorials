from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_in_report = fields.Boolean(
        string="Print Sub-products in Report",
        default=False,
        help="If checked, the individual sub-product components will be printed on the quotation/order report.",
    )

    @api.onchange("order_line")
    def _onchange_order_line(self):
        current_kit_ids = [
            line._origin.id for line in self.order_line if line.product_is_kit
        ]

        new_order_lines = self.order_line.filtered(
            lambda line: not line.parent_kit_line_id.id
            or (line.parent_kit_line_id.id in current_kit_ids)
        )

        self.order_line = new_order_lines

    def _get_order_lines_to_report(self):
        order_lines = super()._get_order_lines_to_report()
        if self.print_in_report:
            return order_lines
        else:
            return order_lines.filtered(lambda line: not line.parent_kit_line_id)

    def _get_invoiceable_lines(self, final=False):
        invoicable_lines = super()._get_invoiceable_lines(final=final)
        print(len(invoicable_lines), "invoicable lines before filter")
        if self.print_in_report:
            print(len(invoicable_lines), "invoicable lines after filter if true")
            return invoicable_lines
        else:
            print(len(invoicable_lines), "invoicable lines after filter")
            return invoicable_lines.filtered(lambda line: not line.parent_kit_line_id)
