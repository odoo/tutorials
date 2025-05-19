# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrderLineDistribution(models.Model):
    _name = 'sale.order.line.distribution'
    _description = "Sale Order Line Distribution"
    _rec_name = 'price_unit'

    source_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string="Sale Order Line Source", required=True, ondelete='cascade')
    target_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string="Sale Order Line Target", required=True, ondelete='cascade')
    price_unit = fields.Float(string="Price Unit",digits='Product Price', required=True)
    color = fields.Integer(related='source_sale_order_line_id.color', string="Color")

    @api.model_create_multi
    def create(self, vals_list):
        for distribution in vals_list:
            target_sale_order_line_id = self.env['sale.order.line'].browse(distribution.get('target_sale_order_line_id'))
            price_unit = target_sale_order_line_id.price_unit + distribution.get('price_unit')
            target_sale_order_line_id.write({'price_unit': price_unit})
        return super().create(vals_list)

    def unlink(self):
        for distribution in self:
            distribution.target_sale_order_line_id.write({'price_unit': distribution.target_sale_order_line_id.price_unit - distribution.price_unit})
            distribution.source_sale_order_line_id.write({'price_unit': distribution.source_sale_order_line_id.price_unit + distribution.price_unit})
        return super().unlink()
