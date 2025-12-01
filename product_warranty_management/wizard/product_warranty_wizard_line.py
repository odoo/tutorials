# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ProductWarrantyWizardLine(models.TransientModel):
    _name = 'product.warranty.wizard.line'
    _description = "Product Warranty Wizard Line"
    
    product_id = fields.Many2one(comodel_name='product.product', string="Product")
    linked_line_id = fields.Many2one(comodel_name='sale.order.line')
    warranty_configuration_id = fields.Many2one(comodel_name='warranty.configuration', string="Year")
    end_date = fields.Date(string="End Date", compute='_compute_end_date')
    warranty_id = fields.Many2one(comodel_name='product.warranty.wizard', string="Add Warranty")
    
    @api.depends('warranty_configuration_id')
    def _compute_end_date(self):
        for warranty_line in self:
            if warranty_line.warranty_configuration_id.validity == 0:
                warranty_line.end_date = ''
            else:
                validity = warranty_line.warranty_configuration_id.validity
                warranty_line.end_date = fields.Date.today() + relativedelta(years=validity)
