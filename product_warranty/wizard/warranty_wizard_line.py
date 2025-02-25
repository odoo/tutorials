from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class WarrantyWizardLine(models.TransientModel):
    _name = 'warranty.wizard.line'
    _description = 'Warranty Wizard Line'

    wizard_id = fields.Many2one(comodel_name='add.warranty.wizard', string='Wizard', required=True)
    sale_order_line = fields.Many2one(comodel_name='sale.order.line', string='Order Line', required=True)
    product_template = fields.Many2one(
        comodel_name='product.template', string='Product', compute='_compute_product_template'
    )
    warranty_config = fields.Many2one(comodel_name='product.warranty.config', string='Warranty Config')
    date_end = fields.Date(string='End Date', compute='_compute_date_end')

    @api.depends('sale_order_line')
    def _compute_product_template(self):
        for line in self:
            if line.sale_order_line:
                line.product_template = line.sale_order_line.product_template_id
            else:
                line.product_template = False


    @api.depends('warranty_config')
    def _compute_date_end(self):
        for line in self:
            line.date_end = datetime.today() + relativedelta(years=line.warranty_config.years)
