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
        
        # Dictionary to track selected warranties per product
        # Key: (product_id, original_line_id)
        # Value: list of (warranty_line, warranty_data) tuples
        product_warranties = {}
        
        # First, check if any product has multiple warranties selected
        for line in self.warranty_lines.filtered(lambda l: l.selected and l.warranty_id):
            warranty_data = next(
                (data[2] for data in context_warranty_lines 
                 if data[2]['warranty_id'] == line.warranty_id.id),
                None
            )
            if not warranty_data:
                continue
                
            product_tmpl = self.env['product.template'].browse(warranty_data['product_id'])
            if not product_tmpl.exists():
                continue
                
            # Find original sale order line for this product
            original_line = self.sale_order_id.order_line.filtered(
                lambda l: l.product_id.product_tmpl_id.id == product_tmpl.id 
                and not f"Valid until" in (l.name or '')
            )
            if not original_line:
                continue
                
            key = (product_tmpl.id, original_line[0].id)
            if key not in product_warranties:
                product_warranties[key] = []
            product_warranties[key].append((line, warranty_data))
        
        # Check for multiple warranties per product
        for (product_id, line_id), warranties in product_warranties.items():
            if len(warranties) > 1:
                product = self.env['product.template'].browse(product_id)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Multiple Warranties Selected',
                        'message': f'Multiple warranties selected for {product.name}. Please select only one warranty per product.',
                        'type': 'warning',
                        'sticky': True,
                    }
                }
        
        if not product_warranties:
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
        
        # Add warranties
        for (product_id, original_line_id), warranties in product_warranties.items():
            warranty_line, warranty_data = warranties[0]  # We know there's only one per product now
            
            # Get original line
            original_line = self.env['sale.order.line'].browse(original_line_id)
            if not original_line.exists():
                continue
                
            # Check if warranty already exists for this product
            existing_warranty = self.sale_order_id.order_line.filtered(
                lambda l: f"For product: {original_line.product_id.name}" in (l.name or '') 
                and f"Valid until" in (l.name or '')
            )
            if existing_warranty:
                continue
            
            # Calculate warranty price
            warranty_price = (warranty_line.warranty_id.percentage * original_line.price_unit) / 100
            
            # Create warranty order line
            new_line = self.sale_order_id.order_line.create({
                'order_id': self.sale_order_id.id,
                'product_id': warranty_line.warranty_id.product_tmpl_id.product_variant_id.id,
                'name': f'{warranty_line.warranty_id.name} - Valid until {warranty_data["end_date"]}\n'
                        f'For product: {original_line.product_id.name}',
                'price_unit': warranty_price,
                'product_uom_qty': original_line.product_uom_qty,
                'product_uom': original_line.product_uom.id
            })
            print(f"Added warranty {warranty_line.warranty_id.name} for product {original_line.product_id.name}")

        return {'type': 'ir.actions.act_window_close'}
