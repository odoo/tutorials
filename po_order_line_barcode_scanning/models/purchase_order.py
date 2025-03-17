from odoo import models
from odoo.exceptions import ValidationError


class PurchaseOrderInherit(models.Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "barcodes.barcode_events_mixin"]

    def on_barcode_scanned(self, barcode):
        self.ensure_one()
        print("Barcode scanned in purchase Order:", barcode)

        # Step 1: Validate if the purchase order exists (order_id should not be empty)
        if not self._origin.id:
            raise ValidationError(
                "Purchase Order is not created. Please create a purchase order first."
            )

        # Step 2: Try to find the product using the barcode
        product = self.env["product.product"].search(
            [("barcode", "=", barcode)], limit=1
        )

        if not product:
            raise ValidationError(
                "Product with this barcode was not found in the database."
            )

        # Step 3: Check if the product is already added to the order, otherwise create a new line
        order_line = self.order_line.filtered(lambda line: line.product_id == product)
        if order_line:
            # Increase the quantity if the product is already in the order
            order_line.product_qty += 1
        else:
            # Create a new purchase order line with the scanned product
            new_line = self.env[
                "purchase.order.line"
            ].create(
                {
                    "order_id": self._origin.id,  # Use the original purchase Order ID (from _origin)
                    "product_id": product.id,
                    "product_qty": 1,  # Start with a quantity of 1
                    "price_unit": product.list_price,  # Or another price field as needed
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
