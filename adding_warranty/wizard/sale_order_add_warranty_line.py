from odoo import api, fields, models
from odoo.tools.date_utils import relativedelta

class SaleOrderAddWarrantyLine(models.TransientModel):
    _name = "sale.order.add.warranty.line"
    _description = "Warranty Selection"

    wizard_id = fields.Many2one(
        "sale.order.add.warranty", required=True, ondelete="cascade"
    )
    sale_order_line_id = fields.Many2one(
        "sale.order.line", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("product.product")
    warranty_id = fields.Many2one("warranty.configuration", string="Warranty Period")
    end_date = fields.Date(string="End Date", compute="_compute_end_date")

    @api.depends("warranty_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_id:
                today = fields.Date.today()
                period = record.warranty_id.period
                period_type = record.warranty_id.period_type

                if period_type == "week":
                    record.end_date = today + relativedelta(weeks=period)
                elif period_type == "month":
                    record.end_date = today + relativedelta(months=period)
                elif period_type == "quarter":
                    record.end_date = today + relativedelta(months=period * 3)
                elif period_type == "year":
                    record.end_date = today + relativedelta(years=period)
                else:
                    record.end_date = today
            else:
                record.end_date = False
