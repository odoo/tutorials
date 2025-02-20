from odoo import models, fields, api

class WarrantySelectionWizard(models.TransientModel):
    _name = 'warranty.selection.wizard'
    _description = 'Warranty Selection Wizard'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    warranty_lines = fields.One2many('warranty.selection.wizard.line', 'wizard_id', string="Warranty Lines")

    def action_add_warranties(self):
        """Add selected warranties to the sale order"""
        print("\n=== Starting warranty addition ===\n")
        print(f"Sale Order ID: {self.sale_order_id.id}")
        
        # Get warranty lines from context
        context_warranty_lines = self.env.context.get('default_warranty_lines', [])
        print(f"Total warranty lines from context: {len(context_warranty_lines)}")
        print(f"Context warranty lines: {context_warranty_lines}")
        
        # Group warranties by product to ensure we only add one warranty per product
        selected_warranties = {}
        for line in self.warranty_lines.filtered(lambda l: l.selected and l.warranty_id):
            # Find matching warranty data from context
            warranty_data = next(
                (data[2] for data in context_warranty_lines 
                 if data[2]['warranty_id'] == line.warranty_id.id),
                None
            )
            if not warranty_data:
                print(f"No context data found for warranty {line.warranty_id.name}")
                continue
                
            print(f"\nProcessing warranty line:")
            print(f"- Warranty Data: {warranty_data}")
            print(f"- Product ID: {warranty_data['product_id']}")
            print(f"- Warranty: {line.warranty_id.name} (ID: {line.warranty_id.id})")
            print(f"- End Date: {warranty_data['end_date']}")
            
            product_tmpl = self.env['product.template'].browse(warranty_data['product_id'])
            if not product_tmpl.exists():
                print(f"Product template {warranty_data['product_id']} not found")
                continue
                
            if warranty_data['product_id'] not in selected_warranties:
                selected_warranties[warranty_data['product_id']] = (line, warranty_data, product_tmpl)
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Multiple Warranties Selected',
                        'message': f'You can only select one warranty per product. Multiple warranties selected for {product_tmpl.name}',
                        'type': 'warning',
                        'sticky': True,
                    }
                }
        
        if not selected_warranties:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Warranties Selected',
                    'message': 'Please select at least one warranty to add.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        for product_tmpl_id, (line, warranty_data, product_tmpl) in selected_warranties.items():
            # Get the original order line for this product
            original_lines = self.sale_order_id.order_line.filtered(
                lambda l: l.product_id.product_tmpl_id.id == product_tmpl_id
            )
            print(f"- Found {len(original_lines)} matching original order lines")
            
            if not original_lines:
                print(f"  No matching order line found for product {product_tmpl.name}, skipping...")
                continue

            original_line = original_lines[0]
            print(f"- Original line: {original_line.product_id.name} (ID: {original_line.product_id.id})")
            print(f"- Original price: {original_line.price_unit}")
            
            # Calculate warranty price
            warranty_price = (line.warranty_id.percentage * original_line.price_unit) / 100
            print(f"- Warranty percentage: {line.warranty_id.percentage}%")
            print(f"- Calculated warranty price: {warranty_price}")
            
            # Create warranty order line
            new_line = self.sale_order_id.order_line.create({
                'order_id': self.sale_order_id.id,
                'product_id': line.warranty_id.product_tmpl_id.product_variant_id.id,
                'name': f'{line.warranty_id.name} - Valid until {warranty_data["end_date"]}\n'
                        f'For product: {original_line.product_id.name}',
                'price_unit': warranty_price,
                'product_uom_qty': original_line.product_uom_qty,
                'product_uom': original_line.product_uom.id,
            })
            print(f"- Created new order line with ID: {new_line.id}")

        print("\n=== Warranty addition completed ===\n")
        return {'type': 'ir.actions.act_window_close'}
