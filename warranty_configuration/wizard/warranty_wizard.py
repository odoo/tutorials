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
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id")
        if not active_id:
            return res

        order = self.env["sale.order"].browse(active_id)

        if not order or not order.exists():
            return res

        warranty_lines = []
        for line in order.order_line:
            if (
                line.product_id.is_warranty_available
                and not line.product_warranty_line_id
            ):
                existing_warranty = order.order_line.filtered(
                    lambda ln: ln.product_warranty_line_id == line
                )
                warranty_config = self.env["warranty.configuration"].search(
                    [("product_id", "=", existing_warranty.product_id.id)], limit=1
                )
                warranty_lines.append(
                    {
                        "order_line_id": line.id,
                        "product_id": line.product_id.id,
                        "warranty_configuration_id": warranty_config.id if warranty_config else False,
                    }
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
        for line in self.warranty_line_ids:
            warranty_price = (
                line.order_line_id.price_unit
                * line.warranty_configuration_id.percentage
                / 100
            )

            existing_warranty = self.env["sale.order.line"].search(
                [
                    ("order_id", "=", self.order_id.id),
                    ("product_warranty_line_id", "=", line.order_line_id.id),
                ],
                limit=1,
            )

            product_line_sequence = line.order_line_id.sequence

            warranty_vals = {
                "order_id": line.order_line_id.order_id.id,
                "product_id": line.warranty_configuration_id.product_id.id,
                "product_warranty_line_id": line.order_line_id.id,  # Original product with warranty link
                "name": f"Warranty: {line.warranty_configuration_id.product_id.name}\nFor {line.order_line_id.product_id.name}\nEnd Date: {line.end_date}",
                "price_unit": warranty_price,
                "product_uom_qty": 1,
                "sequence": product_line_sequence + 1,
            }
            if existing_warranty:
                existing_warranty.write(warranty_vals)  # Update existing warranty line
            elif line.warranty_configuration_id.product_id.id:
                self.env["sale.order.line"].create(
                    warranty_vals
                )  # Create new warranty line


class WarrantyLineWizard(models.TransientModel):
    _name = "warranty.line.wizard"
    _description = "Warranty Line for Wizard"

    wizard_id = fields.Many2one("warranty.wizard", string="Warranty Wizard")
    product_id = fields.Many2one("product.product", string="Product")
    order_line_id = fields.Many2one("sale.order.line", required=True)
    warranty_configuration_id = fields.Many2one(
        "warranty.configuration", string="Warranty Configuration"
    )
    end_date = fields.Date(
        string="End Date", compute="_compute_end_date", store=True, readonly=True
    )

    @api.depends("warranty_configuration_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_configuration_id and record.order_line_id:
                record.end_date = date.today() + timedelta(
                    days=record.warranty_configuration_id.duration_years * 365
                )
            else:
                record.end_date = False
