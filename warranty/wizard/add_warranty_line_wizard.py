from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class AddWarrantyLine(models.TransientModel):
    _name = "add.warranty.line.wizard"
    _description = "Add Warranty Line Wizard"

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        domain=[("is_warranty_available", "=", True)],
    )
    year = fields.Many2one("warranty.config", string="Year")
    end_date = fields.Date(string="End Date", compute="_compute_end_date")
    warranty_line_id = fields.Many2one("add.warranty.wizard", string="Wizard")
    main_order_line = fields.Many2one("sale.order.line", string="Main Order Line")

    @api.depends("year")
    def _compute_end_date(self):
        for record in self:
            record.end_date = fields.Date.to_date(date.today()) + relativedelta(
                years=record.year.duration
            )
