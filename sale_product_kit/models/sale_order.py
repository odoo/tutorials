from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_kit_components = fields.Boolean()

    def _get_order_lines_to_report(self):
        lines = super()._get_order_lines_to_report()
        return lines.filtered(
            lambda l: (
                not l.is_kit_child
                or l.order_id.print_kit_components
            )
        )
