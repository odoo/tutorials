from odoo import api, fields, models
from datetime import date, timedelta


class ProductWarrantyWizard(models.TransientModel):
    _name = "product.warranty.wizard"
    _description = "Product Warranty Wizard"

    year = fields.Many2one("product.warranty", string="year")
    product_template_id = fields.Many2one("product.template", string="Product")
    end_date = fields.Date("End Date", compute="_compute_end_date")
    order_line_id = fields.Many2one("sale.order.line")
    wizard_id = fields.Many2one("order.wizard", required=True)

    @api.depends("year")
    def _compute_end_date(self):
        for line in self:
            line.end_date = date.today() + timedelta(days=365 * line.year.year)
