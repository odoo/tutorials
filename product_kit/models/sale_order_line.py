from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(related="product_id.is_kit", depends=['product_id'])
    parent_kit_id = fields.Many2one(comodel_name='sale.order.line', ondelete='cascade')
    sub_products = fields.One2many(comodel_name='sale.order.line', inverse_name='parent_kit_id')
    sub_product_price = fields.Float()

    def action_add_sub_products(self):
        return {
            'name': f'Product: {self.product_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'kit.add.sub.products.wizard',
            'view_mode': 'form',
            'target': 'new'
        }

    @api.ondelete(at_uninstall=False)
    def _unlink_and_compute_kit_price(self):
        for line in self:
            if line.parent_kit_id:
                line.parent_kit_id.price_unit -= line.sub_product_price * line.product_uom_qty

    @api.onchange('product_id')
    def _onchange_unlink_sub_products(self):
        for line in self:
            if line.sub_products:
                for sub_product in line.sub_products:
                    sub_product.unlink()
            line.price_unit = line.product_id.lst_price
