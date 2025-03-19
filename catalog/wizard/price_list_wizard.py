# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, api, fields, models


class PriceListWizard(models.TransientModel):
    _name = 'price.list.wizard'
    _description = "Price List Wizard"
    
    list_ids = fields.One2many(comodel_name='price.list.wizard.line', inverse_name='list_id', string="Price List")
    
    @api.model
    def default_get(self, fields_list):
        default_fields = super().default_get(fields_list)
        sale_order_line_id = self.env.context.get('active_id', [])
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        price_history_list = self.env['sale.order.line'].search_read(
            domain=[
                ('order_partner_id.id', '=', sale_order_line.order_id.partner_id.id),
                ('product_id.id', '=', sale_order_line.product_id.id),
                ('state', '=', 'sale' ),
                ('id', '!=', sale_order_line.id)
            ],
            fields=['price_unit', 'create_date'],
            limit=5,
            order='create_date DESC'
        )
        link_commands = [
            Command.link(
                self.env['price.list.wizard.line'].sudo().create({
                    'so_date': price['create_date'],
                    'price': price['price_unit'],
                }).id
            )
            for price in price_history_list
        ]
        default_fields['list_ids'] = link_commands
        return default_fields
