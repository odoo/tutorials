from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ProductDisplayWizard(models.TransientModel):
    _name = "product.display.wizard"
    _description = "Product Display Wizard"

    sale_order_id = fields.Many2one(
        "sale.order", string="Sale Order", required=True)
    warranty_line_ids = fields.One2many(
        "add.warranty.line", "warranty_wizard_id")

    def default_get(self, fields):
        # Call the default behavior of the parent model's default_get method to get default values.
        res = super().default_get(fields)

        # Retrieve the currently active sale order (the sale order related to the current context).
        sale_order = self.env["sale.order"].browse(
            self._context.get("active_id"))
        res["sale_order_id"] = sale_order.id

        # Initialize an empty list to store warranty lines.
        warranty_lines = []

        # Loop through each order line in the sale order.
        for line in sale_order.order_line:
            if line.product_id.is_warranty_available:
                warranty_lines.append(
                    (
                        0, 0,
                        {
                            "product_id": line.product_id.id,
                        },
                    )
                )
        res["warranty_line_ids"] = warranty_lines
        return res

    def add_button(self):
        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

        for line in self.warranty_line_ids:
            if line.year_id:
                price = 0
                for record in sale_order.order_line:
                    if record.product_id == line.product_id:
                        price = (record.price_subtotal *
                                 line.year_id.percentage) / 100
                        sale_order.order_line = [(0, 0, {
                            "product_id": line.year_id.product_id.id,
                            "name": "Extended Warranty",
                            "order_id": sale_order.id,
                            "product_uom": 1,
                            "product_uom_qty": 1,
                            "price_unit": price,
                            "tax_id": None,
                            "warranty_product_id": record.id,
                        })]


class AddWarrantyLine(models.TransientModel):
    _name = "add.warranty.line"
    _description = "Add Warranty Line"

    product_id = fields.Many2one('product.product', 'Product')
    year_id = fields.Many2one('warranty.configuration', 'Year', required=True)
    end_date = fields.Date('End Date', compute="_compute_end_date", store=True)
    warranty_wizard_id = fields.Many2one(
        "product.display.wizard", string="Warranty Wizard", required=True)

    @api.depends('year_id')
    def _compute_end_date(self):
        # Computing the end date based on the selected warranty year
        for record in self:
            if record.year_id and record.year_id.years:
                # Compute the end date as today + the number of years in the warranty
                record.end_date = fields.Date.today(
                    self) + relativedelta(years=record.year_id.years)
            else:
                # If no year is selected, end date is set to False
                record.end_date = False
