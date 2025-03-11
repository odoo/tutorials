from odoo import models, fields, api, Command


class ProductWarrantyWizard(models.TransientModel):
    _name = "product.warranty.wizard"
    _description = "This is to add warranty lines in so"

    wizard_line_ids = fields.One2many("product.warranty.lines.wizard", "wizard_id")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_order = self.env["sale.order"].browse(self._context.get("active_id"))
        orders = active_order.order_line.filtered(
            lambda order: order.product_id.is_warranty_available
        )
        res["wizard_line_ids"] = [
            Command.create(
                {
                    "order_line_id": order.id,
                    "product_id": order.product_id.id,
                    "warranty_product_id": order.warranty_product_id.id
                    if order.has_warranty_product
                    else False,
                }
            )
            for order in orders
        ]
        return res

    def add_warranty(self):
        self.ensure_one()
        order_id = self.env.context.get("active_id")
        for line in self.wizard_line_ids:
            if line.warranty_product_id:
                if line.order_line_id.has_warranty_product:
                    if line.warranty_product_id.id == line.order_line_id.warranty_product_id.id:
                        continue
                    else:
                        line.order_line_id.warranty_order_line.write(
                            {
                                "product_id": line.warranty_product_id.product_id.id,
                                "name": f"End Date: {line.end_date}",
                                "price_unit": (
                                    line.order_line_id.price_unit * line.warranty_product_id.percentage
                                ) / 100,
                            }
                        )
                        line.order_line_id.write(
                            {
                                "warranty_product_id": line.warranty_product_id.id,
                            }
                        )
                else:
                    warranty_order_line = self.env["sale.order.line"].create(
                        {
                            "order_id": order_id,
                            "product_id": line.warranty_product_id.product_id.id,
                            "name": f"End Date: {line.end_date}",
                            "product_uom_qty": 1,
                            "price_unit": (
                                line.order_line_id.price_unit * line.warranty_product_id.percentage
                            ) / 100,
                            "is_warranty_product": True,
                            "product_with_warranty_order_line": line.order_line_id.id,
                            "sequence": line.order_line_id.sequence + 1,
                        }
                    )
                    line.order_line_id.write(
                        {
                            "has_warranty_product": True,
                            "warranty_product_id": line.warranty_product_id.id,
                            "warranty_order_line": warranty_order_line,
                        }
                    )
        return True


class ProductWarrantyLinesWizard(models.TransientModel):
    _name = "product.warranty.lines.wizard"
    _description = "This is the lines"

    wizard_id = fields.Many2one("product.warranty.wizard")
    order_line_id = fields.Many2one("sale.order.line", store=True)
    product_id = fields.Many2one("product.product", store=True)
    product_display_name = fields.Char(related="product_id.display_name")
    warranty_product_id = fields.Many2one("warranty.config", string="Year")
    end_date = fields.Date(readonly=True, compute="_compute_end_date")

    @api.depends("warranty_product_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_product_id:
                record.end_date = fields.Date.add(
                    fields.Date.today(), years=record.warranty_product_id.year
                )
            else:
                record.end_date = False
