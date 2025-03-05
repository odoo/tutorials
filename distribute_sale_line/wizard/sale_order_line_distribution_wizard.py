# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class SaleOrderLineDistributionWizard(models.TransientModel):
    _name = 'sale.order.line.distribution.wizard'
    _description = "Sale Order Line Distribution Wizard"

    source_sale_order_line_wizard_id = fields.Many2one(comodel_name='source.sale.order.line.wizard', string="Source Sale Order Line Wizard")
    source_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string="Sale Order Line Source", required=True)
    target_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string="Sale Order Line", required=True)
    price_unit = fields.Float(string="Price Unit", digits='Product Price', required=True)
