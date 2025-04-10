from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class ProductWarrantyWizard(models.TransientModel):
    _name = 'product.warranty.line'
    _description = 'wizard to add warranty line'

    wizard_id = fields.Many2one("add.product.warranty")
    warranty_configuration_id = fields.Many2one("warranty.configuration", string="Add Warranty")
    sale_order_line_id = fields.Many2one("sale.order.line")
    warranty_end_date = fields.Date(compute="_compute_end_date", string="End Date")

    @api.onchange("warranty_configuration_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_configuration_id:
                record.warranty_end_date = fields.Date.today() + relativedelta(years=record.warranty_configuration_id.duration)
            else:
                record.warranty_end_date = fields.Date.today()
