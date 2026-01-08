from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class WarrantyWizardLine(models.TransientModel):
    _name = "warranty.wizard.line"
    _description = "Warranty Wizard Line"

    wizard_id = fields.Many2one("warranty.wizard", string="Wizard")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    product_id = fields.Many2one("product.product", string="Product", readonly=True)
    warranty_configuration_id = fields.Many2one("warranty.configuration", string="Warranty", required=True)
    end_date = fields.Date(string="End Date", compute="_compute_end_date")

    @api.depends("warranty_configuration_id.years")
    def _compute_end_date(self):
        for record in self:
            record.end_date = False
            if record.warranty_configuration_id.years:
                record.end_date = fields.Date.today() + relativedelta(years=record.warranty_configuration_id.years)
