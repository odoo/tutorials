from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class WarrantyAddLine(models.TransientModel):
    _name = "warranty.add.line"

    name = fields.Char(string="Product")
    product_id = fields.Many2one("sale.order.line")
    warranty_id = fields.Many2one("warranty.add")
    year = fields.Many2one("warranty.config")
    end_date = fields.Date(compute="_compute_end_date", readonly=True)

    @api.depends('year')
    def _compute_end_date(self):
        for record in self:
            if record.year is not None:
                record.end_date = fields.Date.today() + relativedelta(years=record.year.period)
