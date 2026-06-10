from odoo import api, Command, fields, models


class SubKitProductWizard(models.TransientModel):
    _name = "sale.kit.product.sub.product.wizard"
    _description = "Sub products view of a kit product"

    sale_line_id = fields.Many2one("sale.order.line")
    wizard_line_ids = fields.One2many(
        "sale.kit.product.wizard.line", "product_wizard_line"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get("active_id")
        sale_line = self.env["sale.order.line"].browse(active_id)
        res["sale_line_id"] = sale_line.id
        sub_product_ids = sale_line.product_id.product_tmpl_id.sub_products
        lines = []
        if sale_line.kit_line_ids:
            for kit_line in sale_line.kit_line_ids:
                lines.append(
                    Command.create(
                        {
                            "product_id": kit_line.product_id.id,
                            "product_qty": kit_line.product_uom_qty,
                            "product_price": kit_line.kit_component_price,
                        }
                    )
                )
        elif sub_product_ids:
            for sub_product in sub_product_ids:
                lines.append(
                    Command.create(
                        {
                            "product_id": sub_product.id,
                            "product_qty": 1,
                            "product_price": sub_product.lst_price,
                        }
                    )
                )
        res.update({"wizard_line_ids": lines})

        return res

    def action_confirm(self):
        self.ensure_one()
        self.sale_line_id.kit_line_ids.unlink()
        total_price = 0
        sub_product_lines = []
        for line in self.wizard_line_ids:
            total_price += line.product_qty * line.product_price
            sub_product_lines.append(
                Command.create(
                    {
                        "order_id": self.sale_line_id.order_id.id,
                        "product_id": line.product_id.id,
                        "product_uom_qty": line.product_qty,
                        "price_unit": 0,
                        "kit_component_price": line.product_price,
                        "parent_kit_line_id": self.sale_line_id.id,
                        "is_sub_product": True,
                    }
                )
            )
        if sub_product_lines:
            self.sale_line_id.order_id.write({"order_line": sub_product_lines})

        if self.sale_line_id.price_unit != total_price:
            self.sale_line_id.update({"price_unit": total_price})

        return {"type": "ir.actions.act_window_close"}
