# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_in_report = fields.Boolean(string="Print in report", default=False)

    @api.onchange('order_line')
    def _onchange_order_line_kit(self):
        delete_commands = link_commands = []
        for line in self.order_line:
            if line.kit_line_id and (line.kit_line_id.id not in self.order_line.ids):
                delete_commands.append(Command.delete(line.id))
            else:
                link_commands.append(Command.link(line.id))
        if delete_commands:
            self.order_line = delete_commands + link_commands

    def action_confirm(self):
        for order in self:
            if order.order_line.filtered(lambda line: line.is_kit and not line.sub_line_ids):
                raise UserError(_("There must be atleast one sub-product line for each kit product line."))
        return super().action_confirm()
