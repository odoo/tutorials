from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class AddWarrantyLine(models.TransientModel):
    _name = "add.warranty.line"

    product_template_id = fields.Many2one("product.template", string="Product")
    warranty_id = fields.Many2one("add.warranty", string="Wizard Reference")
    year = fields.Many2one("warranty.configuration")
    end_date = fields.Date(string="End Date", compute="_compute_end_date")

    @api.depends("year")
    def _compute_end_date(self):
        if self.year:
            self.end_date = date.today() + relativedelta(years=self.year.period)
