# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, Command, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_print = fields.Boolean(string="Print in report?")

    @api.onchange('order_line')
    def _onchange_order(self):
        deleting_line = []
        for line in self.order_line:
            if line.parent_sale_order_line_id:
                if line.parent_sale_order_line_id.id not in self.order_line.ids:
                    deleting_line.append(Command.delete(line.id))
        self.order_line = deleting_line

    def _get_order_lines_to_report(self):
        show_lines = super()._get_order_lines_to_report()
        if self.is_print:
            return show_lines
        else:
            return show_lines.filtered(lambda line: not line.parent_sale_order_line_id)

    def _get_invoiceable_lines(self, final=False):
        if self.is_print:
            return super()._get_invoiceable_lines(final)
        else:
            return super()._get_invoiceable_lines(final).filtered(lambda line: not line.parent_sale_order_line_id)
