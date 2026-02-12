from odoo import models, fields, api

from odoo.fields import Command


class ProductKitWizard(models.TransientModel):
    _name = "product.kit.wizard"
    _description = "Kit Sub Product Wizard"

    sale_line_id = fields.Many2one("sale.order.line")
    main_product_id = fields.Many2one("product.product", string="Product")
    line_ids = fields.One2many("kit.wizard.line", "wizard_id", string="Sub Products")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_line = self.env["sale.order.line"].browse(self._context.get("active_id"))
        if sale_line.product_id:
            product = sale_line.product_id
            sale_order = sale_line.order_id
            kit_sub_product = []
            for sub in product.product_tmpl_id.sub_product:
                existing_line = sale_order.order_line.filtered(
                    lambda line: line.product_id == sub
                                 and line.kit_parent_line_id == sale_line
                )
                # existing_line = self.env["sale.order.line"].search([
                #     ("order_id", "=", sale_order.id),
                #     ("product_id", "=", sub.id),
                #     ("kit_parent_line_id", "=", sale_line.id),
                # ], limit=1)

                kit_sub_product.append(
                    Command.create(
                        {
                            "product_id": sub.id,
                            "quantity": existing_line.product_uom_qty if existing_line else 1.0,
                            "price": existing_line.extra_price if existing_line else sub.lst_price,
                            # "existing_line_id": existing_line.id if existing_line else False,
                        }
                    )
                )

            res.update(
                {
                    "main_product_id": product.id,
                    "sale_line_id": sale_line.id,
                    "line_ids": kit_sub_product,
                }
            )
        return res

    def action_confirm(self):
        order = self.sale_line_id.order_id
        Parent_kit_product_line = self.sale_line_id
        parent_product = Parent_kit_product_line.product_id
        parent_sequence = Parent_kit_product_line.sequence
        total_price = parent_product.list_price
        for wizard_line in self.line_ids:
            existing_line = order.order_line.filtered(
                lambda line: line.product_id == wizard_line.product_id
                             and line.kit_parent_line_id == Parent_kit_product_line

            )
            # existing_line = self.env["sale.order.line"].search([
            #     ("order_id", "=", order.id),
            #     ("product_id", "=", wizard_line.product_id.id),
            #     ("kit_parent_line_id", "=", Parent_kit_product_line.id),
            # ], limit=1)
            values = {
                "product_uom_qty": wizard_line.quantity,
                "price_unit": 0.0,
                "extra_price": wizard_line.price,
                "sequence": parent_sequence,
            }

            if existing_line:
                existing_line.write(values)
            else:
                self.env["sale.order.line"].create(
                    {
                        **values,
                        "name": wizard_line.product_id.name,
                        "order_id": order.id,
                        "product_id": wizard_line.product_id.id,
                        "is_kit_product": True,
                        "kit_parent_line_id": Parent_kit_product_line.id,
                    }
                )

            total_price += wizard_line.price * wizard_line.quantity

        Parent_kit_product_line.write({"price_unit": total_price})
