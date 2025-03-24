from odoo import _, models
from odoo.exceptions import UserError, ValidationError


class PurchaseOrderInherit(models.Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "barcodes.barcode_events_mixin"]

    def on_barcode_scanned(self, barcode):
        self.ensure_one()
        print("Barcode scanned in Purchase Order:", barcode)

        # Step 1: Validate if the purchase order exists (order_id should not be empty) used origin cause self.id returns <newID object>
        if not self._origin.id:
            raise UserError(
                _(
                    "Purchase Order is not created. Please create a purchase order first."
                )
            )

        # Step 2: Check if the purchase order state is 'cancel' or 'done', raise an error if so
        if self.state in ["cancel", "done"]:
            raise UserError(
                _(
                    "This purchase order is either canceled or locked. You cannot add any more products."
                )
            )

        # Step 3: Try to find the product using the barcode
        product = self.env["product.product"].search([("barcode", "=", barcode)])

        if not product:
            raise ValidationError(
                _("Product with this barcode was not found in the database.")
            )

        # Step 4: Check if the product is already added to the order, otherwise create a new line
        order_line = self.order_line.filtered(lambda line: line.product_id == product)

        if order_line:
            # Increase the quantity if the product is already in the order
            first_line = order_line[
                0
            ]  # Get the first line if there are multiple lines for the same product
            first_line.product_qty += 1
        else:
            # Create a new purchase order line with the scanned product
            new_line = self.env["purchase.order.line"].new(
                {
                    "order_id": self.id,  # Use the original Purchase Order ID
                    "product_id": product.id,
                    "product_qty": 1,  # Start with a quantity of 1
                    "price_unit": product.list_price,  # Or another price field as needed
                    "name": product.name,  # Set the mandatory 'name' field (description)
                    "product_uom": product.uom_id.id,  # Set the valid unit of measure
                }
            )

            # Add the new line to the purchase order dynamically
            self.write(
                {
                    "order_line": [
                        (4, new_line.id)
                    ]  # This adds the new line dynamically to the order
                }
            )

        print("Purchase order line updated with product:", product.name)
