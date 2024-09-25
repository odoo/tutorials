from odoo import models, fields, api, Command
from dateutil.relativedelta import relativedelta


class AddWarranty(models.TransientModel):
    _name = "add.warranty"
    _description = "Add Warranty Wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", required=True)
    warranty_line_ids = fields.One2many("add.warranty.line", "warranty_wizard_id")

    def default_get(self, fields):
        res = super().default_get(fields)
        sale_order = self.env["sale.order"].browse(self._context.get("active_id"))
        res["sale_order_id"] = sale_order.id
        warranty_lines = []
        for line in sale_order.order_line:
            if line.product_id.is_warranty_available:
                warranty_lines.append(Command.create({"product_id": line.product_id.id}))
        res["warranty_line_ids"] = warranty_lines
        return res

    def add_warranty(self):

        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

        for line in self.warranty_line_ids:
            if line.warranty_id:
                price = 0
                for record in sale_order.order_line:
                    if record.product_id == line.product_id:
                        price = (record.price_subtotal * line.warranty_id.percentage) / 100
                        sale_order.order_line = [Command.create({
                            "product_id": line.warranty_id.product_id.id,
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

    warranty_wizard_id = fields.Many2one(
        "add.warranty", string="Warranty Wizard", required=True
    )
    product_id = fields.Many2one("product.product", string="Product", required=True)
    warranty_id = fields.Many2one("warranty.config", string="Warranty years", required=True)
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)

    @api.depends("warranty_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_id:
                time_years = record.warranty_id.years
                record.end_date = fields.Date.context_today(self) + relativedelta(
                    years=time_years
                )
