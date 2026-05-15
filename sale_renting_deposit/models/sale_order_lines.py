from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_deposit_line = fields.Boolean(default=False)
    deposit_origin_line_id = fields.Many2one('sale.order.line', ondelete='cascade')

    def _get_line_header(self):
        if self.is_deposit_line and self.name:
            return self.name
        return super()._get_line_header()

    @api.model_create_multi
    def create(self, vals_list):
        order_lines = super().create(vals_list)
        for line in order_lines:
            if (line.product_id.deposit_required and not line.is_deposit_line):
                deposit_product_param = self.env["ir.config_parameter"].sudo().get_param(
                    "sale_renting.deposit_product_id"
                )
                deposit_product_id = int(deposit_product_param)
                deposit_amount = line.product_id.deposit_amount
                self.create({
                    'order_id': line.order_id.id,
                    'product_id': deposit_product_id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': deposit_amount,
                    'name': f"Deposit for {line.product_id.name}",
                    'is_deposit_line': True,
                    'deposit_origin_line_id': line.id,
                })
        return order_lines

    def write(self, vals):
        res = super().write(vals)
        deposit_lines = self.env['sale.order.line'].search(
            [('deposit_origin_line_id', 'in', self.ids)]
        )
        for line in self:
            if line.is_deposit_line:
                continue
            deposit_line = deposit_lines.filtered(
                lambda l: l.deposit_origin_line_id == line
            )
            if not deposit_line:
                continue
            deposit_line.write({
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.product_id.deposit_amount,
                'name': f"Deposit for {line.product_id.name}",
            })
        return res
