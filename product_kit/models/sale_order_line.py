from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit_product = fields.Boolean(related="product_template_id.is_kit")
    parent_line_id = fields.Many2one(comodel_name='sale.order.line', name="Linked kit product line", ondelete="cascade", domain="[('order_id', '=', order_id)]")

    @api.ondelete(at_uninstall=False)
    def _unlink_all_sub_product_lines(self):
        kit_lines = self.filtered(lambda l: l.product_id.is_kit)
        if kit_lines:
            self.search([('parent_line_id', 'in', kit_lines.ids)]).unlink()

    kit_wizard_button = fields.Char(string="Kit Wizard Button")
    