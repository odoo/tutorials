# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, api, fields, models
from odoo.exceptions import UserError

class SourceSaleOrderLineWizard(models.TransientModel):
    _name = 'source.sale.order.line.wizard'
    _description = "Source Sale Order Line Wizard"

    source_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string="Source Sale Order Line", required=True, readonly=True)
    source_price_unit = fields.Float(related='source_sale_order_line_id.price_unit', string="Original Unit Price")
    sale_order_line_distribution_wizard_ids = fields.One2many(
        comodel_name='sale.order.line.distribution.wizard',
        inverse_name='source_sale_order_line_wizard_id',
        string="Distributions"
    )
    distributed_price_unit = fields.Float(
        compute='_compute_distributed_price_unit',
        digits='Product Price',
        string="Distributed Unit Price",
        help="Sum of all distributed unit prices."
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        
        source_sale_order_line_id = self.env.context.get('active_id')
        source_sale_order_line = self.env['sale.order.line'].browse(source_sale_order_line_id)
        target_sale_order_line_ids = source_sale_order_line.order_id.order_line.filtered(lambda r: r.is_included_in_distribution).filtered(lambda r: r != source_sale_order_line).ids
        if not target_sale_order_line_ids:
            raise UserError("No sale order lines are available for distributions. Please include some sale order line for distribution.")
        price_unit = source_sale_order_line.price_unit/len(target_sale_order_line_ids)

        distribution_wizards = [{
            'source_sale_order_line_id': source_sale_order_line_id,
            'target_sale_order_line_id': order_line,
            'price_unit': price_unit
        } for order_line in target_sale_order_line_ids]

        distribution_wizards = self.env['sale.order.line.distribution.wizard'].create(distribution_wizards)
        defaults.update({'sale_order_line_distribution_wizard_ids': [Command.set(distribution_wizards.ids)]})
        defaults.update({'source_sale_order_line_id': source_sale_order_line_id})
        return defaults

    @api.depends('sale_order_line_distribution_wizard_ids.price_unit')
    def _compute_distributed_price_unit(self):
        for source_sale_order_line_wizard in self:
            source_sale_order_line_wizard.distributed_price_unit = sum(source_sale_order_line_wizard.sale_order_line_distribution_wizard_ids.mapped('price_unit'))

    def action_distribute(self):
        for source_sale_order_line_wizard in self:
            distribution_wizards = source_sale_order_line_wizard.sale_order_line_distribution_wizard_ids
            if not distribution_wizards:
                raise UserError("No sale order lines are available for distributions. Please include some sale order line for distribution.")
            source_sale_order_line = source_sale_order_line_wizard.source_sale_order_line_id

            total_distributed_price = sum(distribution_wizards.mapped('price_unit'))
            if total_distributed_price > source_sale_order_line.price_unit:
                raise UserError("Total distributed price cannot be greater than current sale order line's Unit Price.")
            source_price_unit = source_sale_order_line.price_unit - total_distributed_price
            source_sale_order_line.write({'price_unit': source_price_unit})

            distributions = [{
                'source_sale_order_line_id': distribution_wizard.source_sale_order_line_id.id,
                'target_sale_order_line_id': distribution_wizard.target_sale_order_line_id.id,
                'price_unit': distribution_wizard.price_unit,
            } for distribution_wizard in distribution_wizards]

            self.env['sale.order.line.distribution'].create(distributions)
        return True
