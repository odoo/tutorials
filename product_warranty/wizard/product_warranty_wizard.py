from datetime import date, timedelta
from odoo import api, fields, models


class ProductWarrantyWizard(models.TransientModel):
    _name = "product.warranty.wizard"
    _description = "Product Warranty Wizard"

    year = fields.Many2one("product.warranty", string="year")
    product_template_id = fields.Many2one("product.template", string="Product")
    enddate = fields.Date("End Date", compute="_compute_enddate")
    order_line_id = fields.Many2one("sale.order.line")
    wizard_id = fields.Many2one("order.wizard")

    @api.depends("year")
    def _compute_enddate(self):
        for line in self:
            line.enddate = date.today() + timedelta(days=365 * line.year.year)
