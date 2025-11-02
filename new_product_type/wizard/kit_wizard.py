from odoo import fields, models, api, Command
from odoo.exceptions import UserError

class KitWizard(models.TransientModel):
    _name = "kit.wizard"
    _description = "Kit Wizard"

    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line", required=True)
    product_id = fields.Many2one("product.product", string="Kit Product", required=True)
    sub_product_ids = fields.One2many("kit.wizard.line", "wizard_id", string="Sub Products")

    @api.model
    def default_get(self, fields_list):
        # Pre-fill the wizard with existing sub-ptoducts.
        res = super().default_get(fields_list)
        sale_order_line_id = self.env.context.get("default_sale_order_line_id")
        if not sale_order_line_id:
            return res
        
        sale_order_lines = self.env["sale.order.line"].browse(sale_order_line_id)
        sub_products = []
        # Check if wizard has previously stored prices.
        prev_wizard = self.search([("sale_order_line_id", "=", sale_order_line_id)], order="id desc", limit=1)
        # If previous wizard exists, use its stored sub-products
        if prev_wizard:
            sub_products = [
                Command.create({
                    "product_id": subproduct.product_id.id,
                    "quantity": subproduct.quantity,
                    "price": subproduct.price,
                    "order_line_id": subproduct.order_line_id.id,
                }) for subproduct in prev_wizard.sub_product_ids
            ]
        # Otherwise, get from product template
        elif sale_order_lines.product_id.is_kit:
            sub_products = [
                Command.create({
                    "product_id": kit_product.id,
                    "quantity": 1.0,
                    "price": kit_product.lst_price,
                }) for kit_product in sale_order_lines.product_id.kit_product_ids
            ]

        res.update(
                    {
                        "product_id": sale_order_lines.product_id.id,  # Main kit product.
                        "sub_product_ids": sub_products,  # Load sub-products using Command.create.
                    }
                )        
        return res

    def unlink(self):
        """Delete kit components when the main product is deleted."""
        for line in self:
            if line.is_kit_product and line.kit_subproduct_ids:
                # Delete all related kit components.
                line.kit_subproduct_ids.unlink()
                
        # Delete the main product line itself.
        return super(SaleOrderLine, self).unlink()
    
    def action_confirm(self):
        # Confirm the selection of sub-products and update sale order lines.
        sale_order_line_id = self.sale_order_line_id.id

        sale_order_lines = self.env["sale.order.line"].browse(sale_order_line_id)
        sale_order = sale_order_lines.order_id

        original_main_product_price = sale_order_lines.product_id.lst_price

        existing_sub_products = {line.product_id.id: line for line in sale_order_lines.kit_subproduct_ids}
        updated_sub_products = []
        total_price = 0

        for sub_product in self.sub_product_ids:
            if sub_product.product_id.id in existing_sub_products:
                existing_line = existing_sub_products[sub_product.product_id.id]
                # Update existing component
                updated_sub_products.append(
                    Command.update(
                        existing_line.id,
                        {
                            "product_uom_qty": sub_product.quantity,
                            "price_unit": 0.0,
                        },
                    )
                )
            else:
                # Add new component
                updated_sub_products.append(
                    Command.create(
                        {
                            "product_id": sub_product.product_id.id,
                            "price_unit": 0.0,
                            "product_uom_qty": sub_product.quantity,
                            "order_id": sale_order_lines.order_id.id,
                            "product_uom": sub_product.product_id.uom_id.id,
                            "name": sub_product.product_id.name or "Kit Component",
                            "parent_line_id": sale_order_lines.id,  # Link to main kit line
                        }
                    )
                )
            total_price += sub_product.price * sub_product.quantity

        if updated_sub_products:
            sale_order_lines.write({"kit_subproduct_ids": updated_sub_products})

        # Update kit price (sum of all sub-products)
        new_main_product_price = original_main_product_price + total_price
        sale_order_lines.write({"price_unit": new_main_product_price})

        return True

class KitWizardLine(models.TransientModel):
    _name = "kit.wizard.line"
    _description = "Kit Wizard Line"

    wizard_id = fields.Many2one("kit.wizard", string="Wizard", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", required=True, string="Component")
    quantity = fields.Float(string="Quantity", default=1.0)
    price = fields.Float(string="Price")
    order_line_id = fields.Many2one("sale.order.line", string="Existing Order Line")
