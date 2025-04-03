from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import date

class WarrantyWizard(models.TransientModel):
    _name="product.warranty.line"
    _description="Wizard to warranty line"

    wizard_id = fields.Many2one(comodel_name="add.product.warranty")
    warranty_configuration_id = fields.Many2one(comodel_name="warranty.configuration")
    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line")

    warranty_end_date = fields.Date(compute="_compute_warranty_end_date", string="End Date")

    @api.depends("warranty_configuration_id.duration")
    def _compute_warranty_end_date(self):
        for record in self:
            if record.warranty_configuration_id:
                record.warranty_end_date = fields.Date.today() + relativedelta(years=record.warranty_configuration_id.duration)
            else:
                record.warranty_end_date = fields.Date.today()
