from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    linked_line_id = fields.Many2one('sale.order.line', string="Linked Line", copy=False, readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        sale_order_lines = super(SaleOrderLine, self).create(vals_list)
        deposit_lines_to_create = []

        for line in sale_order_lines:
            if line.product_id.product_tmpl_id.is_deposit:
                deposit_product = line.order_id.company_id.extra_deposit
                if deposit_product:
                    deposit_amount = line.product_id.product_tmpl_id.deposit_amount * line.product_uom_qty
                    deposit_lines_to_create.append({
                        'order_id': line.order_id.id,
                        'product_id': deposit_product.id,
                        'product_uom_qty': 1,
                        'price_unit': deposit_amount,
                        'linked_line_id': line.id,
                        'sequence': line.sequence + 1,  
                    })
        if deposit_lines_to_create:
            self.env['sale.order.line'].create(deposit_lines_to_create)
        return sale_order_lines


    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        for line in self:
            if line.product_id.product_tmpl_id.is_deposit:
                deposit_line = self.env['sale.order.line'].search([
                    ('order_id', '=', line.order_id.id),
                    ('linked_line_id', '=', line.id),
                ])
                if deposit_line:
                    deposit_line.price_unit = line.product_id.product_tmpl_id.deposit_amount * line.product_uom_qty
        return res

    def unlink(self):
        for line in self:
            if line.product_id.product_tmpl_id.is_deposit:
                deposit_line = self.env['sale.order.line'].search([
                    ('order_id', '=', line.order_id.id),
                    ('linked_line_id', '=', line.id),
                ])
                if deposit_line:
                    deposit_line.unlink()
        return super(SaleOrderLine, self).unlink()
