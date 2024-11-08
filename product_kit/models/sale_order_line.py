from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(related='product_template_id.is_kit', store=True, default=False)
    parent_id = fields.Many2one('sale.order.line', ondelete='cascade')
    secondary_price_unit = fields.Float()

    @api.onchange('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'price_total')
    def recalculate_price_total(self):
        self.price_subtotal = (self.product_id.lst_price * self.product_uom_qty)
        subproducts = self.env['sale.order.line'].search([('parent_id', '=', self.id)])
        for prod in subproducts:
            self.price_subtotal = self.price_subtotal + (prod.secondary_price_unit * prod.product_uom_qty)
