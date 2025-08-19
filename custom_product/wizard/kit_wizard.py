from odoo import fields, models, api, Command
from odoo.exceptions import UserError


class KitWizard(models.TransientModel):
    _name = "kit.wizard"
    _description = "Kit Wizard"

    sale_order_line_id = fields.Many2one(
        "sale.order.line", string="Sale Order Line", required=True
    )
    product_id = fields.Many2one("product.product", string="Kit Product", required=True)
    component_ids = fields.One2many(
        "kit.wizard.line", "wizard_id", string="Sub Products"
    )

    @api.model
    def default_get(self, fields_list):
        """Pre-fill the wizard with existing sub-products or default kit components."""
        res = super().default_get(fields_list)
        sale_order_line_id = self.env.context.get("default_sale_order_line_id")
        if not sale_order_line_id:
            return res

        sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
        components = []

        # Load existing sub-products if available
        if sale_order_line.kit_component_ids:
            for component in sale_order_line.kit_component_ids:
                components.append(
                    Command.create(
                        {
                            "product_id": component.product_id.id,
                            "quantity": component.product_uom_qty,
                            "price": component.price_unit,
                            "order_line_id": component.id,  # Store existing line ID
                        }
                    )
                )
        # Otherwise, generate from product template
        elif sale_order_line.product_id.is_kit:
            for kit_product in sale_order_line.product_id.kit_product_ids:
                components.append(
                    Command.create(
                        {
                            "product_id": kit_product.id,
                            "quantity": 1.0,
                            "price": kit_product.lst_price,
                        }
                    )
                )
                print(components)

        res.update(
            {
                "product_id": sale_order_line.product_id.id,  # Main kit product
                "component_ids": components,  # Load sub-products using Command.create
            }
        )
        return res

    def action_confirm(self):
        """Confirm the selection of sub-products and update sale order lines."""
        sale_order_line_id = self.sale_order_line_id.id

        if not sale_order_line_id:
            return {"type": "ir.actions.act_window_close"}

        sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
        sale_order = sale_order_line.order_id

        existing_components = {
            line.product_id.id: line for line in sale_order_line.kit_component_ids
        }
        updated_components = []

        for sub_product in self.component_ids:
            if sub_product.product_id.id in existing_components:
                # Update existing component
                updated_components.append(
                    Command.update(
                        existing_components[sub_product.product_id.id].id,
                        {
                            "product_uom_qty": sub_product.quantity,
                            "price_unit": sub_product.price,
                        },
                    )
                )
            else:
                # Add new component
                updated_components.append(
                    Command.create(
                        {
                            "product_id": sub_product.product_id.id,
                            "price_unit": 0.0,
                            "product_uom_qty": sub_product.quantity,
                            "order_id": sale_order_line.order_id.id,
                            "product_uom": sub_product.product_id.uom_id.id,
                            "name": sub_product.product_id.name or "Kit Component",
                            "parent_line_id": sale_order_line.id,  # Link to main kit line
                        }
                    )
                )

        if updated_components:
            sale_order_line.write({"kit_component_ids": updated_components})

        # Update kit price (sum of all sub-products)
        kit_price = sum(sub.quantity * sub.price for sub in self.component_ids)
        sale_order_line.write({"price_unit": kit_price})

        return True


class KitWizardLine(models.TransientModel):
    _name = "kit.wizard.line"
    _description = "Kit Wizard Line"

    wizard_id = fields.Many2one(
        "kit.wizard", string="Wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("product.product", required=True, string="Component")
    quantity = fields.Float(string="Quantity", default=1.0)
    price = fields.Float(string="Price")
    order_line_id = fields.Many2one("sale.order.line", string="Existing Order Line")

    @api.model_create_multi
    def create(self, vals):
        print("INSIDE OVERRIDE CREATE")
        print(self.wizard_id)
        print(vals)
        return super().create(vals)
