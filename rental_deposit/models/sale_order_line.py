from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    linked_line_id = fields.Many2one('sale.order.line', string='Linked Product Line')

    @api.model_create_multi
    def create(self, vals):
        lines = super().create(vals)
        for line in lines:
            deposit_product_id = int(self.env['ir.config_parameter'].sudo().get_param('rental_deposit.deposit_product', default=0))
            if line.product_id.id != deposit_product_id and line.product_id.rent_ok and line.product_id.deposit_require:
                line.order_id._add_deposit_product(line)
        return lines

    def write(self, vals):
        res = super().write(vals)
        for line in self:
            if 'product_uom_qty' in vals and line.product_id.deposit_require:
                line.order_id._add_deposit_product(line)
        return res
