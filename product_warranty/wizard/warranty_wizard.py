from odoo import api, fields, models

class WarrantyWizard(models.TransientModel):
    _name = 'warranty.wizard'
    _description = 'Map SO with warranty lines'

    sale_order_id= fields.Many2one('sale.order', string="Sale Order")
    warranty_line_ids= fields.One2many('warranty.line.wizard', 'wizard_id', string="Warranty Lines")

    # Automatically fill warranty_line_ids from SO line
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get('active_id')   #active sale order ID
    
        if active_id:
            sale_order = self.env['sale.order'].browse(active_id)
            if not sale_order:
                return res
            
            warranty_lines = []
            for line in sale_order.order_line:
                isWarrantyAvailable = self.env['sale.order.line'].search([('linked_line_id', '=',line.id )])
                if line.product_template_id and line.product_template_id.is_warranty_available and not isWarrantyAvailable:
                    warranty_lines.append((0, 0, {
                        'sale_order_line_id': line.id,
                        'product_id': line.product_template_id.id,
                    }))
                    
            res.update({
                'sale_order_id': sale_order.id,
                'warranty_line_ids': warranty_lines,
            })
        return res
    

    # Insert warranty product in current SO lines
    def action_add_warranty(self):
        warranty_product_list = []
        for record in self:
            sale_order = record.sale_order_id  
            for line in record.warranty_line_ids:
                if line.warranty_config_id:  
                    warranty_product_list.append({
                        "order_id": sale_order.id,
                        "name": f"{line.warranty_config_id.name} / {line.end_date}",
                        "product_id": line.warranty_config_id.warranty_product.product_variant_id.id,  
                        "price_unit": line.sale_order_line_id.price_subtotal
                                    * (line.warranty_config_id.percentage / 100),  
                        "linked_line_id": line.sale_order_line_id.id,
                        "sequence": line.sale_order_line_id.sequence,  
                    })
        breakpoint()
        self.env['sale.order.line'].create(warranty_product_list)
