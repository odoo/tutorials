from odoo import models, fields, api


class RentalOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_deposit_line = fields.Boolean(default=False)
    linked_deposit_line_id = fields.Many2one('sale.order.line')

    @api.model_create_multi
    def create(self, vals_list):
        order_lines = super().create(vals_list)

        for line in order_lines:
            if (line.product_id.is_deposit and not line.is_deposit_line):
                product_id_txt = self.env['ir.config_parameter'].sudo().get_param('sale_renting.deposit_product_id')
                product_id = int(product_id_txt)
                amount_to_deposit = line.product_id.deposit_amount

                self.create({
                    'product_id': product_id,
                    'name': f"Deposit for {line.product_id.name}",
                    'order_id': line.order_id.id,
                    'price_unit': amount_to_deposit,
                    'product_uom_qty': line.product_uom_qty,
                    'is_deposit_line': True,
                    'linked_deposit_line_id': line.id
                })

        return order_lines

    @api.ondelete(at_uninstall=False)
    def _unlink_order_line(self):
        deposits = self.env["sale.order.line"].search(
            [("linked_deposit_line_id", "in", self.ids)]
        )
        if deposits:
            deposits.unlink()
        return True

    def write(self, vals):
        result = super().write(vals)
        deposit_lines = self.env['sale.order.line'].search([('linked_deposit_line_id', 'in', self.ids)])

        for line in self:
            if (line.is_deposit_line):
                continue

            filtered_deposit_line = deposit_lines.filtered(lambda d_line: d_line.linked_deposit_line_id == line)

            if not filtered_deposit_line:
                continue
            filtered_deposit_line.write({
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.product_uom_qty * line.product_id.deposit_amount

            })
        return result
