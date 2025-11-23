# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class WarrantyLineWizard(models.TransientModel):
    _name = 'warranty.line.wizard'

    warranty_wizard_id = fields.Many2one(comodel_name='warranty.wizard')
    product_id = fields.Many2one(comodel_name='product.product', string="Product", readonly=True)
    end_date = fields.Date(string="End Date", compute='_compute_end_date', readonly=True)
    warranty_configuration_id = fields.Many2one(comodel_name='warranty.configuration', string="Year")
    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line')

    @api.depends('warranty_configuration_id')
    def _compute_end_date(self):
        for warranty_line in self:
            warranty_line.end_date = (fields.Date.today() + relativedelta(years=warranty_line.warranty_configuration_id.validity)) if warranty_line.warranty_configuration_id else ""
