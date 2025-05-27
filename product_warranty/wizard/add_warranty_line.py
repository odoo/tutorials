from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class AddWarrantyLine(models.TransientModel):
    _name = "add.warranty.line"
    _description = "Warranty Line for Wizard"

    wizard_id = fields.Many2one(
        "product.add.warranty", string="Wizard", ondelete="cascade"
    )
    product_id = fields.Many2one("product.product", string="Product", required=True)
    order_line_id = fields.Many2one(
        "sale.order.line", required=True, ondelete="cascade"
    )
    warranty_period = fields.Integer(
        string="Warranty Period (Years)", related="warranty_id.years", store=True
    )
    warranty_id = fields.Many2one(
        "product.warranty.configuration", string="Select Warranty"
    )
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    price_unit = fields.Float(string="Warranty Price")

    @api.depends("warranty_period")
    def _compute_end_date(self):
        for line in self:
            if line.warranty_period:
                line.end_date = date.today() + relativedelta(years=line.warranty_period)
            else:
                line.end_date = False
