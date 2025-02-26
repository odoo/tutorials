from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class WarrantyWizardLine(models.TransientModel):
    _name = 'warranty.wizard.line'
    _description = 'Warranty Wizard Line'

    wizard_id = fields.Many2one(comodel_name='add.warranty.wizard', string="Wizard", required=True)
    sale_order_line = fields.Many2one(comodel_name='sale.order.line', string="Order Line", required=True)
    product_template = fields.Many2one(
        string="Product", related='sale_order_line.product_template_id',
    )
    warranty_config = fields.Many2one(comodel_name='product.warranty.config', string="Warranty Config")
    date_end = fields.Date(string="End Date", compute='_compute_date_end')

    @api.depends('warranty_config')
    def _compute_date_end(self):
        for line in self:
            line.date_end = datetime.today() + relativedelta(years=line.warranty_config.years)
