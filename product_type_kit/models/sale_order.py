from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_kit_details = fields.Boolean(string="Print Kit Details")
    display_in_report = fields.Boolean(string="Print in report?", default=True)

    @api.model
    def unlink(self):
        for order in self:
            for line in order.order_line:
                if not line.is_subproduct:
                    # delete sub lines linked to this main line
                    sub_lines = order.order_line.filtered(lambda l: l.kit_parent_line_id == line.id)
                    sub_lines.unlink()
        return super().unlink()
