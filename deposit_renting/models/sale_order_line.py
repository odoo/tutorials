from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_deposit_line = fields.Boolean(string="Is Deposit Line", default=False)

    def _add_deposit_line(self):
        deposit_product_id = int(self.env['ir.config_parameter'].get_param('deposit_product_id'))
        deposit_product = self.env['product.product'].browse(deposit_product_id)
        for line in self:
            if line.order_id and line.product_id.rent_ok and line.product_id.require_deposit:
                deposit_line = line.order_id.order_line.filtered(lambda line: line.linked_line_id == self.id)
                if deposit_line:
                    deposit_line.product_uom_qty = line.product_uom_qty
                    deposit_line.price_unit = line.product_id.deposit_amount
                else:
                    self.env["sale.order.line"].create({
                        'order_id': line.order_id.id,
                        'product_id': deposit_product.id,
                        'name': f"Deposit For {line.product_id.name}",
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit': line.product_id.deposit_amount,
                        'linked_line_id': line.id,
                        'price_subtotal': line.product_uom_qty * line.product_id.deposit_amount,
                        'is_deposit_line': True,
                    })

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res._add_deposit_line()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'product_uom_qty' in vals:
            for line in self:
                linked_lines = self.search([('linked_line_id', '=', line.id)])
                for linked_line in linked_lines:
                    linked_line.product_uom_qty = line.product_uom_qty
                    linked_line.price_subtotal = line.product_uom_qty * line.product_id.deposit_amount
        
        return res
