from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _update_deposit_lines(self):
        if self.env.context.get('skip_deposit_update'):
            return

        deposit_product_id = self.env['ir.config_parameter'].sudo().get_param('deposit_rental.deposit_id')

        if not deposit_product_id:
            return

        deposit_product_tmpl = self.env['product.template'].browse(int(deposit_product_id))

        if deposit_product_tmpl.exists():
            deposit_product = deposit_product_tmpl.product_variant_id
        else:
            deposit_product = self.env['product.product'].browse(int(deposit_product_id))

        if not deposit_product:
            return

        deposit_lines = self.order_line.filtered(lambda line: line.product_id.id == deposit_product.id)

        deposit_total = 0
        rented_products = []

        for line in self.order_line.filtered(lambda l: l.product_id.product_tmpl_id.deposit_required):
            deposit_total += line.product_id.deposit_amount * line.product_uom_qty
            rented_products.append(line.product_id.display_name)

        deposit_description = "\nDeposit for " + ", ".join(rented_products)

        if deposit_product_tmpl.exists():
            deposit_product_tmpl.sudo().write({'description_sale': deposit_description})

        if deposit_product.exists():
            deposit_product.sudo().write({'description_sale': deposit_description})

        if deposit_total > 0:
            if deposit_lines:
                deposit_lines[0].with_context(skip_deposit_update=True).write({
                    'product_uom_qty': 1, 
                    'price_unit': deposit_total,
                    'name': deposit_description,
                })
            else:
                self.with_context(skip_deposit_update=True).write({
                    'order_line': [(0, 0, {
                        'product_id': deposit_product.id,
                        'product_uom_qty': 1,
                        'price_unit': deposit_total,
                        'name': deposit_description,
                    })]
                })
        elif deposit_lines:
            deposit_lines.with_context(skip_deposit_update=True).unlink()
