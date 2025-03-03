from odoo import api, fields, models
from odoo.fields import Command


class SubProductKitWizard(models.TransientModel):
    _name = "sub.product.kit.wizard"
    _description = "Sub products Kit selection Wizard"

    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale order line")
    product_id = fields.Many2one("product.product", string="Product", required=True)
    kit_component_ids = fields.One2many(
        "sub.product.kit.wizard.line", "wizard_id", string="Sub Products"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_line_id = self.env.context.get("active_id")
        sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)

        if sale_order_line.product_id:
            product = sale_order_line.product_id
            sale_order = sale_order_line.order_id

            existing_lines = sale_order.order_line.filtered(
                lambda line: line.product_id in product.sub_product_ids
                and line.kit_parent_id == sale_order_line
            )

            kit_component_commands = []

            for sub_product in product.sub_product_ids:
                existing_line = existing_lines.filtered(
                    lambda line: line.product_id == sub_product
                )

                if existing_line:
                    existing_line = existing_line[0]

                kit_component_commands.append(
                    Command.create(
                        {
                            "product_id": sub_product.id,
                            "quantity": existing_line.product_uom_qty if existing_line else 1.0,
                            "price": existing_line.extra_price if existing_line else sub_product.lst_price,
                            "existing_line_id": existing_line.id if existing_line else False,
                        }
                    )
                )

            res.update(
                {
                    "product_id": product.id,
                    "sale_order_line_id": sale_order_line.id,
                    "kit_component_ids": kit_component_commands,
                }
            )

        return res

    def confirm_kit(self):
        order = self.sale_order_line_id.order_id
        main_product_line = self.sale_order_line_id
        main_product = main_product_line.product_id
        parent_sequence = main_product_line.sequence
        total_price = main_product.list_price

        for component in self.kit_component_ids:
            existing_line = order.order_line.filtered(
                lambda line: line.product_id == component.product_id
                and line.kit_parent_id == main_product_line
                and line.order_id == order
            )
            values = {
                "product_uom_qty": component.quantity,
                "price_unit": 0.0,
                "extra_price": component.price,
                "sequence": parent_sequence,
            }

            if existing_line:
                existing_line.write(values)
            else:
                self.env["sale.order.line"].create(
                    {
                        **values,
                        "name": component.product_id.name,
                        "order_id": order.id,
                        "product_id": component.product_id.id,
                        "is_kit_component": True,
                        "kit_parent_id": main_product_line.id,
                    }
                )

            total_price += component.price * component.quantity

        main_product_line.write({"price_unit": total_price})
