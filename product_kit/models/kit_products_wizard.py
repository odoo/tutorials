from odoo import models, fields, api


class KitProductsWizardLine(models.TransientModel):
    _name = "kit.products.wizard.line"
    _description = "Kit Products Wizard Line"

    wizard_line_id = fields.Many2one("kit.products.wizard", required=True)
    product_id = fields.Many2one("product.product", string="Product")
    product_quantity = fields.Float(string="Quantity")
    price = fields.Float(string="Unit Price")


class KitProductsWizard(models.TransientModel):
    _name = "kit.products.wizard"
    _description = "Kit Products Wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", readonly=True)
    product_template_id = fields.Many2one("product.template", string="Product", readonly=True)
    subProduct_ids = fields.One2many("kit.products.wizard.line", "wizard_line_id", string="Sub Products")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_id = self.env.context.get("default_sale_order_id")
        product_template_id = self.env.context.get("default_product_template_id")

        res.update({
            "sale_order_id": sale_order_id,
            "product_template_id": product_template_id,
        })

        if sale_order_id and product_template_id:
            product_template = self.env["product.template"].browse(product_template_id)
            sub_products = product_template.subProduct_ids

            existing_lines = self.env["sale.order.line"].search([
                ("order_id", "=", sale_order_id),
                ("product_id", "in", sub_products.ids)
            ])

            line_data = []
            for sub_product in sub_products:
                existing_line = existing_lines.filtered(lambda l: l.product_id.id == sub_product.id)
                line_data.append((0, 0, {
                    "product_id": sub_product.id,
                    "product_quantity": existing_line.product_uom_qty if existing_line else 1,
                    "price": existing_line.last_updated_price if existing_line else sub_product.list_price,
                }))

            res["subProduct_ids"] = line_data

        return res

    def action_open_wizard_popup(self):
        self.ensure_one()

        so_line_model = self.env["sale.order.line"]
        total_price = 0.0

        for sub in self.subProduct_ids:
            sub_total = sub.product_quantity * sub.price
            total_price += sub_total

            line_vals = {
                "product_uom_qty": sub.product_quantity,
                "price_unit": 0.0,
                "last_updated_price": sub.price,
            }

            existing_line = so_line_model.search([
                ("order_id", "=", self.sale_order_id.id),
                ("product_id", "=", sub.product_id.id),
                ("is_subProduct", "=", True),
            ], limit=1)

            if existing_line:
                existing_line.write(line_vals)
            else:
                line_vals.update({
                    "name": sub.product_id.name,
                    "order_id": self.sale_order_id.id,
                    "product_id": sub.product_id.id,
                    "is_subProduct": True,
                })
                so_line_model.create(line_vals)

        main_product = self.product_template_id.product_variant_id
        main_line = so_line_model.search([
            ("order_id", "=", self.sale_order_id.id),
            ("product_id", "=", main_product.id),
        ], limit=1)

        if main_line:
            main_line.price_unit = total_price * main_line.product_uom_qty
        else:
            so_line_model.create({
                "order_id": self.sale_order_id.id,
                "product_id": main_product.id,
                "product_uom_qty": 1,
                "price_unit": total_price,
                "name": self.product_template_id.name,
            })

        return {"type": "ir.actions.act_window_close"}
