from odoo import fields, models, api, Command
from odoo.exceptions import UserError

class KitWizard(models.TransientModel):
    _name = "kit.wizard"
    _description = "Kit Wizard"

    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line", required=True)
    product_id = fields.Many2one("product.product", string="Kit Product", required=True)
    component_ids = fields.One2many("kit.wizard.line", "wizard_id", string="Sub Products")

    @api.model
    def default_get(self, fields_list):
        """Pre-fill the wizard with existing sub-products or default kit components."""
        res = super().default_get(fields_list)  
        sale_order_line_id = self.env.context.get("default_sale_order_line_id")
        if not sale_order_line_id:
            return res
        
        sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
        components = []
        # Check if wizard has previously stored prices
        prev_wizard = self.search([("sale_order_line_id", "=", sale_order_line_id)], order="id desc", limit=1)
        if prev_wizard:
            for component in prev_wizard.component_ids:
                components.append(
                    Command.create({
                        "product_id": component.product_id.id,
                        "quantity": component.quantity,
                        "price": component.price,
                        "order_line_id": component.order_line_id.id,
                    })
                )
        else:
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

    def unlink(self):
        """Delete kit components when the main product is deleted."""
        for line in self:
            if line.is_kit_product and line.kit_component_ids:
                # Delete all related kit components
                line.kit_component_ids.unlink()
                
        # Delete the main product line itself
        return super(SaleOrderLine, self).unlink()
    
    def action_confirm(self):
        """Confirm the selection of sub-products and update sale order lines."""
        sale_order_line_id = self.sale_order_line_id.id

        if not sale_order_line_id:
            return {"type": "ir.actions.act_window_close"}

        sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
        sale_order = sale_order_line.order_id

        original_main_product_price = sale_order_line.product_id.lst_price

        existing_components = {line.product_id.id: line for line in sale_order_line.kit_component_ids}
        updated_components = []
        total_price = 0

        for sub_product in self.component_ids:
            if sub_product.product_id.id in existing_components:
                existing_line = existing_components[sub_product.product_id.id]

                # Keep the last edited price
                # last_price = existing_line.price_unit if existing_line.price_unit != 0.0 else sub_product.price
                
                # calculate price diff
                # if existing_line.product_uom_qty != sub_product.quantity:
                #     price_diff = sub_product.price * (sub_product.quantity - existing_line.product_uom_qty)
                #     price_difference += price_diff

                # Update existing component
                updated_components.append(
                    Command.update(
                        existing_line.id,
                        {
                            "product_uom_qty": sub_product.quantity,
                            "price_unit": 0.0,
                        },
                    )
                )
                # price_difference += last_price * sub_product.quantity
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
                # price_difference += sub_product.price * sub_product.quantity
            total_price += sub_product.price * sub_product.quantity
        if updated_components:
            sale_order_line.write({"kit_component_ids": updated_components})

        # Update kit price (sum of all sub-products)
        # kit_price = sum(sub.quantity * sub.price for sub in self.component_ids)
        # total_price = sale_order_line.price_unit + price_difference
        new_main_product_price = original_main_product_price + total_price
        sale_order_line.write({"price_unit": new_main_product_price})

        return True

class KitWizardLine(models.TransientModel):
    _name = "kit.wizard.line"
    _description = "Kit Wizard Line"

    wizard_id = fields.Many2one("kit.wizard", string="Wizard", required=True, ondelete="cascade")
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