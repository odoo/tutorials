# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    deposit_line_id = fields.Many2one(comodel_name='sale.order.line', help="Order line for deposit amount of this rental product", copy=False)
    rental_line_id = fields.Many2one(comodel_name='sale.order.line', help="Order line of rental product for this deposit amount", copy=False, ondelete="cascade")

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if line.product_id.is_deposit_required:
                deposit_line = self.env['sale.order.line'].create({
                    'order_id': line.order_id.id,
                    'product_id': self.env.company.deposit_product.id,
                    'product_uom_qty': 1,
                    'price_unit': line.product_id.deposit_amount * line.product_uom_qty,
                    'name': f"For {line.product_id.name}",
                    'rental_line_id': line.id,
                })
                line.deposit_line_id = deposit_line.id
        return lines

    @api.depends('rental_line_id.product_uom_qty')
    def _compute_price_unit(self):
        super()._compute_price_unit()
        for line in self:
            if line.rental_line_id:
                print(line.rental_line_id.id, line.rental_line_id.product_id.deposit_amount, line.rental_line_id.product_uom_qty)
                line.price_unit = line.rental_line_id.product_id.deposit_amount * line.rental_line_id.product_uom_qty

    def get_description_following_lines(self):
        if self.product_id.id == self.env.company.deposit_product.id:
            return self.name.splitlines()
        return super().get_description_following_lines()

    def _is_not_sellable_line(self):
        if self.product_id.id == self.env.company.deposit_product.id:
            return True
        return super()._is_not_sellable_line()
