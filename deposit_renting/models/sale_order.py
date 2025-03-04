from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    require_deposit_config = fields.Boolean(string="Require Deposit Configuration", default=False, compute="_compute_has_deposit_line_without_config", help="Has line that require deposit, without configuring the deposit product in settings.")

    @api.depends('order_line')
    def _compute_has_deposit_line_without_config(self):
        deposit_product_id = self.env['ir.config_parameter'].get_param('deposit_product_id')
        for sale_order in self:
            has_line_require_deposit_config = True if len(sale_order.order_line.filtered(lambda line: line.product_id.require_deposit)) > 0 else False
            if has_line_require_deposit_config and not deposit_product_id:
                sale_order.require_deposit_config = True
            else:
                sale_order.require_deposit_config = False
