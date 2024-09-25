from odoo import models, fields, api, Command
from dateutil.relativedelta import relativedelta


class AddWarranty(models.TransientModel):
    _name = "add.warranty"
    _description = "Add Warranty Wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", required=True)
    warranty_line_ids = fields.One2many("add.warranty.line", "warranty_wizard_id")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
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
        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

        # Iterate over warranty lines from the wizard
        for line in self.warranty_line_ids:
            if line.warranty_years:
                for order_line in sale_order.order_line:
                    # Find the product in the sale order line
                    if order_line.product_id == line.product_id:
                        # Calculate the warranty price based on the original product line subtotal
                        price = (
                            order_line.price_subtotal * line.warranty_years.percentage
                        ) / 100

                        # Append the warranty as a separate sale order line without removing the product
                        sale_order.order_line = [
                            Command.create(
                                {
                                    "name": f"Extended Warranty\nEnd date: {line.end_date}",
                                    "order_id": sale_order.id,
                                    "product_id": line.warranty_years.product_id.id,  # Use the warranty product
                                    "product_uom": 1,
                                    "product_uom_qty": 1,
                                    "price_unit": price,
                                    "warranty_product_id": order_line.id,
                                    "tax_id": None,  # You can adjust tax settings here if needed
                                }
                            )
                        ]


class AddWarrantyLine(models.TransientModel):
    _name = "add.warranty.line"
    _description = "Add Warranty Line"

    warranty_wizard_id = fields.Many2one(
        "add.warranty", string="Warranty Wizard", required=True
    )
    product_id = fields.Many2one("product.product", string="Product", required=True)
    warranty_years = fields.Many2one(
        "warranty.config", string="Warranty Period", required=True
    )
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)

    @api.depends("warranty_years")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_years:
                time_period = record.warranty_years.period
                record.end_date = fields.Date.context_today(self) + relativedelta(
                    years=time_period
                )
