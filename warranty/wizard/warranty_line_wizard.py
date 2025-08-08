# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, api, fields, models

class WarrantyLineWizard(models.TransientModel):
    _name = 'warranty.line.wizard'
    _description = "Warranty line wizard"

    wizard_id = fields.Many2one(comodel_name='warranty.wizard', string="Wizard")
    product_id = fields.Many2one(comodel_name='product.product', string="Product")
    warranty_configuration_id = fields.Many2one(comodel_name='warranty.configuration', string="Year")
    end_date = fields.Date(compute='_compute_warranty_date', readonly=True, store=True, string="End Date")
    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string="Sale Order Line")

    @api.depends('warranty_configuration_id')
    def _compute_warranty_date(self):
        for line in self:
            line.end_date = fields.Date.add(fields.Date.today(), years=line.warranty_configuration_id.validity)
