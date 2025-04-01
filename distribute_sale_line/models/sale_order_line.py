# Part of Odoo. See LICENSE file for full copyright and licensing details.

from random import randint

from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _default_color(self):
        return randint(1, 11)

    is_included_in_distribution = fields.Boolean("Include for Distribution", default=True)
    source_sale_order_line_distribution_ids = fields.One2many(
        comodel_name='sale.order.line.distribution',
        inverse_name='source_sale_order_line_id',
        string="Source Sale Order Line Distribution"
    )
    target_sale_order_line_distribution_ids = fields.One2many(
        comodel_name='sale.order.line.distribution',
        inverse_name='target_sale_order_line_id',
        string="Target Sale Order Line Distribution"
    )
    color = fields.Integer(string="Color", default=_default_color)

    def action_open_distribute_sale_order_line_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': "Distribute Sale Order Line Price",
            'res_model': 'source.sale.order.line.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    def unlink(self):
        for sale_order_line in self:
            for source_distribution in sale_order_line.source_sale_order_line_distribution_ids:
                target_sale_order_line = source_distribution.target_sale_order_line_id
                target_price_unit = target_sale_order_line.price_unit - source_distribution.price_unit
                target_sale_order_line.write({'price_unit': target_price_unit})

            for target_distribution in sale_order_line.target_sale_order_line_distribution_ids:
                source_sale_order_line = target_distribution.source_sale_order_line_id
                source_price_unit = source_sale_order_line.price_unit + target_distribution.price_unit
                source_sale_order_line.write({'price_unit': source_price_unit})
        return super().unlink()
