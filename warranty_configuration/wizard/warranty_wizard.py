from datetime import date, timedelta

from odoo import api, Command, fields, models

class WarrantryWizard(models.TransientModel):
    _name = "warranty.wizard"
    _description = "Warranty Wizard"

    order_id = fields.Many2one("sale.order", string="Sale Order", required=True)
    warranty_line_ids = fields.One2many(
        "warranty.line.wizard", "wizard_id", string="Warranty Lines"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get("active_id")

        if not active_id:
            return res

        order = self.env["sale.order"].browse(active_id)

        if not order or not order.exists():
            return res

        warranty_lines = []
        for line in order.order_line:
            if line.product_id.is_warranty_available and not line.product_warranty_id:
                warranty_lines.append(
                    {"order_line_id": line.id, "product_id": line.product_id.id}
                )

        res.update(
            {
                "order_id": order.id,
                "warranty_line_ids": [Command.clear()]
                + [Command.create(vals) for vals in warranty_lines],
            }
        )

        return res

    def action_confirm(self):
        order_lines = []
        for line in self.warranty_line_ids:
            warranty_price = (
                line.order_line_id.price_unit
                * line.warranty_configuration_id.percentage
                / 100
            )
            product_line_sequence = line.order_line_id.sequence
            order_lines.append(
                {
                    "order_id": line.order_line_id.order_id.id,
                    "product_id": line.warranty_configuration_id.product_id.id,
                    "product_warranty_id": line.order_line_id.product_id.id,  # Original product with warranty link
                    "name": f"Warranty: {line.warranty_configuration_id.product_id.name}\nFor {line.order_line_id.product_id.name}\nEnd Date: {line.end_date}",
                    "price_unit": warranty_price,
                    "product_uom_qty": 1,
                    "sequence": product_line_sequence + 1,
                }
            )
            
            if order_lines:
                self.env["sale.order.line"].create(order_lines)
            return


class WarrantyLineWizard(models.TransientModel):
    _name = "warranty.line.wizard"
    _description = "Warranty Line for Wizard"

    wizard_id = fields.Many2one("warranty.wizard", string="Warranty Wizard")
    product_id = fields.Many2one("product.product", string="Product")
    order_line_id = fields.Many2one("sale.order.line")
    warranty_year_id = fields.Many2one("warranty.year", string="Warranty Duration")

    # Linking the warranty configuration that is calculated based on warranty year
    warranty_configuration_id = fields.Many2one(
        "warranty.configuration",
        compute="_compute_warranty_configuration",
        string="Warranty Configuration",
        store=True,
    )
    end_date = fields.Date(
        string="End Date", compute="_compute_end_date", store=True, readonly=True
    )
    price_unit = fields.Float(string="Warranty Price")

    @api.depends("warranty_year_id")
    def _compute_warranty_configuration(self):
        for record in self:
            warranty = self.env["warranty.configuration"].search(
                [
                    ("warranty_year_id", "=", record.warranty_year_id.id),
                ],
                limit=1,
            )
            record.warranty_configuration_id = warranty

    @api.depends("warranty_year_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_year_id:
                record.end_date = date.today() + timedelta(
                    days=record.warranty_year_id.years * 365
                )
            else:
                record.end_date = False
