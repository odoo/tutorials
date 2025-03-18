from odoo import models
from odoo.exceptions import ValidationError

class SaleOrderInherit(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        self.ensure_one()
        print("Barcode scanned in Sale Order:", barcode)

        # Step 1: Validate if the sale order exists (order_id should not be empty)
        if not self._origin.id:
            raise ValidationError("Sale Order is not created. Please create a sale order first.")
        
        # Step 2: Try to find the product using the barcode
        product = self.env['product.product'].search([('barcode', '=', barcode)], limit=1)
        
        if not product:
            raise ValidationError("Product with this barcode was not found in the database.")
        
        # Step 3: Check if the product is already added to the order, otherwise create a new line
        order_line = self.order_line.filtered(lambda line: line.product_id == product)

        if order_line:
            # Increase the quantity if the product is already in the order
            first_line = order_line[0] #get the first line if there exists multiple products within a line
            first_line.product_uom_qty += 1
        else:
            # Create a new sale order line with the scanned product
            #why use new instead of create? I have used new here because when I used create it used to create a bug whenever I cancelled the button and hit reload it used to fetch the saved database items.
            #What used to happen create->stored in database->cancel changes to remove products-> reload page -> fetched data from database->products appear again.
            #What happens after new->stored locally(unsaved not in database)->cancel remove products->reload page->fetch data from database(which is empty because create does not save it)->unsaved products dont appear anymore.
            
            
            new_line = self.env['sale.order.line'].new({
                'order_id': self._origin.id,  # Use the original Sale Order ID (from _origin)
                'product_id': product.id,
                'product_uom_qty': 1,  # Start with a quantity of 1
                'price_unit': product.list_price,  # Or another price field as needed
            })

            # Add the new line to the sale order dynamically
            #i.e when I scan this adds the product lines in real time instead of refresh of the page.
            self.write({
                'order_line': [(4, new_line.id)]  # This adds the new line dynamically to the order
            })
            print("inside else statement!")

        print("Sales order line updated with product:", product.name)

