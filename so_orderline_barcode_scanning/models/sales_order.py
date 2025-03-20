from odoo import models
from odoo.exceptions import UserError, ValidationError  # Use ValidationError for missing product

class SaleOrderInherit(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        self.ensure_one()
        print("Barcode scanned in Sale Order:", barcode)

        # Step 1: Validate if the sale order exists (order_id should not be empty)
        if not self._origin.id:
            raise UserError("Sale Order is not created. Please create a sale order first.")
        
        # Step 2: Check if the sale order state is 'cancel', raise an error if so
        if self.state == 'cancel':
            raise UserError("This sale order is canceled. You cannot add any more products.")

        # Step 3: Try to find the product using the barcode
        product = self.env['product.product'].search([('barcode', '=', barcode)], limit=1)

        if not product:
            raise ValidationError("Product with this barcode was not found in the database.")

        # Step 4: Check if the product is already added to the order, otherwise create a new line
        order_line = self.order_line.filtered(lambda line: line.product_id == product)

        if order_line:
            # Increase the quantity if the product is already in the order
            first_line = order_line[0]  # Get the first line if there are multiple lines for the same product
            first_line.product_uom_qty += 1
        else:
            # Create a new sale order line with the scanned product
            new_line = self.env['sale.order.line'].new({
                'order_id': self._origin.id,  # Use the original Sale Order ID (from _origin)
                'product_id': product.id,
                'product_uom_qty': 1,  # Start with a quantity of 1
                'price_unit': product.list_price,  # Or another price field as needed
            })

            # Add the new line to the sale order dynamically
            self.write({
                'order_line': [(4, new_line.id)]  # This adds the new line dynamically to the order
            })
            print("Inside else statement!")

        print("Sales order line updated with product:", product.name)
