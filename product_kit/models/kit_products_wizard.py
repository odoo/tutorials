from odoo import models, fields, api


class KitProductsWizard(models.TransientModel):
    _name = "kit.products.wizard"
    _description = "Kit Products Wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", readonly=True)
    product_template_id = fields.Many2one("product.template", string="Product", readonly=True)
    kit_product_ids = fields.One2many("kit.products.wizard.line", "wizard_id", string="Sub Products")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        sale_order_id = self.env.context.get("default_sale_order_id")
        product_template_id = self.env.context.get("default_product_template_id")

        if sale_order_id:
            res["sale_order_id"] = sale_order_id

        if product_template_id:
            res["product_template_id"] = product_template_id
            product_template = self.env["product.template"].browse(product_template_id)

            existing_lines = self.env["sale.order.line"].search([
                ("order_id", "=", sale_order_id),
                ("product_id", "in", product_template.kit_product_ids.ids)
            ])

            kit_product_vals = []
            if existing_lines:
                for line in existing_lines:
                    kit_product_vals.append((0, 0, {
                        "product_id": line.product_id.id,
                        "product_qty": line.product_uom_qty,
                        "price_unit": line.product_id.list_price,
                    }))
            else:
                for kit_product in product_template.kit_product_ids:
                    kit_product_vals.append((0, 0, {
                        "product_id": kit_product.id,
                        "product_qty": 1,
                        "price_unit": kit_product.list_price,
                    }))

            res["kit_product_ids"] = kit_product_vals

        return res

    def action_generate_order_lines(self):
        """Updates or creates sale order lines for each kit product in the wizard"""
        self.ensure_one()

        main_product_line = self.env["sale.order.line"].search([
            ("order_id", "=", self.sale_order_id.id),
            ("product_id", "in", self.product_template_id.product_variant_ids.ids),
        ], limit=1)

        original_price = self.product_template_id.list_price
        total_price = original_price

        for kit_product in self.kit_product_ids:
            existing_line = self.env["sale.order.line"].search([
                ("order_id", "=", self.sale_order_id.id),
                ("product_id", "=", kit_product.product_id.id),
                ("from_wizard", "=", True),
            ], limit=1)

            sub_total = kit_product.product_qty * kit_product.product_id.list_price
            total_price += sub_total

            if existing_line:
                existing_line.write({
                    "product_uom_qty": kit_product.product_qty,
                    "price_unit": 0.00,  # Ensure sub-products remain zero-priced
                })
            else:
                self.env["sale.order.line"].create({
                    "name": kit_product.product_id.name,
                    "order_id": self.sale_order_id.id,
                    "product_id": kit_product.product_id.id,
                    "product_uom_qty": kit_product.product_qty,
                    "price_unit": 0.00,
                    "from_wizard": True,
                })

        if main_product_line:
            main_product_line.price_unit = total_price * main_product_line.product_uom_qty
        else:
            self.env["sale.order.line"].create({
                "order_id": self.sale_order_id.id,
                "product_id": self.product_template_id.product_variant_id.id,
                "product_uom_qty": 1,
                "price_unit": total_price,
                "name": self.product_template_id.name,
            })

        return {"type": "ir.actions.act_window_close"}
