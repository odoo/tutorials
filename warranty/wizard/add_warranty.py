from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import re


class AddWarranty(models.TransientModel):
    _name = "add.warranty"
    _description = "Add Warranty Wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", required=True)
    warranty_line_ids = fields.One2many("add.warranty.line", "warranty_wizard_id")

    @api.model
    def default_get(self, fields):
        res = super(AddWarranty, self).default_get(fields)
        sale_order = self.env["sale.order"].browse(self._context.get("active_id"))
        res["sale_order_id"] = sale_order.id

        # Prepare warranty lines from the sale order
        warranty_lines = []
        for line in sale_order.order_line:
            if line.product_id.warranty_available:
                warranty_lines.append(
                    (
                        0,
                        0,
                        {
                            "product_id": line.product_id.id,
                        },
                    )
                )
        res["warranty_line_ids"] = warranty_lines
        return res

    def add_warranty(self):
        sales_order = self.env["sale.order"].browse(self._context.get("active_id"))
        for line in self.warranty_line_ids:
            if line.warranty_id:
                # Calculate warranty price based on the warranty percentage
                warranty_price = sales_order.amount_total * (
                    line.warranty_id.percentage / 100
                )

                # Create new warranty lines in the sale order
                self.env["sale.order.line"].create(
                    {
                        "name": f"Extended Warranty \nEnd Date:{line.end_date} Warranty",
                        "order_id": sales_order.id,
                        "product_id": line.warranty_id.product_id.id,
                        "product_uom_qty": 1,
                        "price_unit": warranty_price,
                    }
                )


class AddWarrantyLine(models.TransientModel):
    _name = "add.warranty.line"
    _description = "Add Warranty Line"

    warranty_wizard_id = fields.Many2one(
        "add.warranty", string="Warranty Wizard", required=True
    )
    product_id = fields.Many2one("product.product", string="Product", required=True)
    warranty_id = fields.Many2one(
        "warranty.config", string="Warranty Period", required=True
    )
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)

    @api.depends("warranty_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_id:
                time_period = record.warranty_id.period
                record.end_date = fields.Date.context_today(self) + relativedelta(
                    years=time_period
                )
