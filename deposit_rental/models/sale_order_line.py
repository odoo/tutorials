from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_deposit_line = fields.Boolean(
        string="Is Deposit Line",
        default=False,
        help="Indicates if this line is for the deposit"
    )
    deposit_of_line_id = fields.Many2one(
        'sale.order.line',
        string="Deposit of Line",
        copy=False
    )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)

        new_deposit_vals_list = []
        for line in lines:
            if line.product_id and not line.is_deposit_line and line.product_id.requires_deposit:
                deposit_product_id = self.env['ir.config_parameter'].sudo().get_param('rental_deposit.deposit_product_id')
                if deposit_product_id:
                    deposit_vals = {
                        'order_id': line.order_id.id,
                        'product_id': int(deposit_product_id),
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit': line.product_id.deposit_amount,
                        'name': f"Deposit for {line.product_id.name}",
                        'is_deposit_line': True,
                        'deposit_of_line_id': line.id,
                    }
                    new_deposit_vals_list.append(deposit_vals)

        if new_deposit_vals_list:
            self.create(new_deposit_vals_list)

        return lines

    def unlink(self):
        deposit_lines_to_delete = self.env['sale.order.line'].search([
            ('deposit_of_line_id', 'in', self.ids)
        ])

        if deposit_lines_to_delete:
            deposit_lines_to_delete.unlink()

        return super().unlink()
