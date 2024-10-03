from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class AddWarranty(models.TransientModel):
    _name = "warranty.wizard"
    _description = "Warranty Wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", required=True)
    warranty_line_ids = fields.One2many("add.warranty.lines", "warranty_wizard_id")

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        sale_order = self.env["sale.order"].browse(self._context.get("active_id"))
        result["sale_order_id"] = sale_order.id

        warranty_lines = []
        for line in sale_order.order_line:
            print(line)
            if line.product_id.is_warranty_available:
                warranty_lines.append(
                    (
                        0,
                        0,
                        {
                            "product_id": line.product_id.id,
                        },
                    )
                )
        result["warranty_line_ids"] = warranty_lines
        return result


class AddWarrantyLine(models.TransientModel):
    _name = "add.warranty.lines"
    _description = "Add Warranty Line"

    warranty_wizard_id = fields.Many2one(
        "warranty.wizard", string="Warranty Wizard", required=True
    )
    product_id = fields.Many2one("product.product", string="Product", required=True)
    year = fields.Many2one("storewarranty.configuration", string="Period")
    end_date = fields.Date(string="End Date", compute="_onchange_year", store=True)

    @api.onchange("year.period")
    def _onchange_year(self):
        if self.year:
            self.end_date = date.today() + relativedelta(years=self.year.period)
        else:
            self.end_date = False
