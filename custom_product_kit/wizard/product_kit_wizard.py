from odoo import api, fields, models, Command


class ProductKitWizard(models.TransientModel):
    _name = "product.kit.wizard"
    _description = "Product kit wizard view"

    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    subproduct_ids = fields.One2many(
        comodel_name="subproduct.line.wizard",
        inverse_name="wizard_id",
        string="Sub Products",
    )
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    kit_line_id = fields.Many2one("sale.order.line", string="Kit Line")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        product_id = self.env.context.get("default_product_id")
        sale_order_id = self.env.context.get("default_sale_order_id")
        kit_line_id = self.env.context.get("default_kit_line_id")

        product = self.env["product.product"].browse(product_id)
        sale_order = self.env["sale.order"].browse(sale_order_id)
        kit_line = self.env["sale.order.line"].browse(kit_line_id)

        sub_product_lines = []
        for sub_product in product.sub_product_ids:
            existing_line = sale_order.order_line.filtered(
                lambda line: line.product_id == sub_product
                and line.kit_line_id == kit_line
            )

            sub_product_lines.append(
                Command.create(
                    {
                        "product_id": sub_product.id,
                        "quantity": existing_line.product_uom_qty if existing_line else 1,
                        "unit_price": existing_line.extra_price if existing_line and existing_line.extra_price > 0 else sub_product.lst_price,
                    }
                )
            )
        res.update(
            {
                "subproduct_ids": sub_product_lines,
                "kit_line_id": kit_line_id,
            }
        )

        return res

    def action_confirm_kit(self):
        sale_order = self.sale_order_id
        sale_order_line_obj = self.env["sale.order.line"]

        kit_line = self.kit_line_id
        kit_price = self.product_id.lst_price

        for subproduct in self.subproduct_ids:
            existing_line = sale_order.order_line.filtered(
                lambda line: line.product_id == subproduct.product_id
                and line.kit_line_id == kit_line
            )
            values = {
                "product_uom_qty": subproduct.quantity,
                "price_unit": 0.0,
                "extra_price": subproduct.unit_price,
            }
            if existing_line:
                existing_line.write(values)
            else:
                values.update(
                    {
                        "order_id": sale_order.id,
                        "product_id": subproduct.product_id.id,
                        "name": subproduct.product_id.name,
                        "is_subproduct": True,
                        "sequence": kit_line.sequence,
                        "kit_line_id": kit_line.id,
                    }
                )
                sale_order_line_obj.create(values)

            kit_price += subproduct.quantity * subproduct.unit_price

        kit_line.write({"price_unit": kit_price})
