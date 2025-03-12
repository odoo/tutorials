# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SalePriceHistoryWizard(models.TransientModel):
    _name = 'sale.price.history.wizard'
    _description = 'Sales Price History'

    product_id = fields.Many2one('product.product')
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    history_line_ids = fields.One2many('sale.price.history.line', 'wizard_id', string="Price History")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        product_id = self.env.context.get('default_product_id')
        partner_id = self.env.context.get('default_partner_id')
        res.update({
            'product_id': product_id,
            'partner_id': partner_id,
        })
        if product_id and partner_id:
            history_lines = []
            sale_order_lines = self.env['sale.order.line'].search([
                ('order_partner_id', '=', partner_id),
                ('product_id', '=', product_id),
                ('state', 'in', ['sale'])],
                order='id desc', limit=5
            )
            for line in sale_order_lines:
                history_lines.append((0, 0, {
                    'order_date': line.order_id.date_order,
                    'price_unit': line.price_unit,
                }))

        res['history_line_ids'] = history_lines
        return res

class SalePriceHistoryLine(models.TransientModel):
    _name = 'sale.price.history.line'
    _description = 'Sales Price History Line'

    wizard_id = fields.Many2one('sale.price.history.wizard', string="Wizard")
    order_date = fields.Datetime(string="Sale Order Date")
    price_unit = fields.Float(string="Sales Price")
