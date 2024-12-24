from odoo import models, fields, api

class WarrantyWizard(models.TransientModel):
    _name = 'warranty.wizard'
    _description = 'Warranty Wizard'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    warranty_line_ids = fields.One2many('warranty.line.wizard', 'wizard_id', string="Warranty Lines")

    @api.model
    def default_get(self, fields):
        res = super(WarrantyWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            sale_order = self.env['sale.order'].browse(active_id)
            if not sale_order:
                return res

            warranty_lines = []
            for line in sale_order.order_line:
                if line.product_template_id and line.product_template_id.is_warranty:
                    warranty_lines.append((0, 0, {
                        'sale_order_line_id': line.id,
                        'product_id': line.product_template_id.id,
                    }))

            res.update({
                'sale_order_id': sale_order.id,
                'warranty_line_ids': warranty_lines,
            })
        return res
    
    def action_add_warranty(self):
        new_order_line_list = []
        for record in self:
            sale_order = record.sale_order_id  
            for line in record.warranty_line_ids:
                if line.warranty_config_id:  
                    new_order_line_list.append({
                        "order_id": sale_order.id,
                        "name": f"{line.warranty_config_id.name} / {line.end_date}",
                        "product_id": line.warranty_config_id.product_id.product_variant_id.id,  
                        "price_unit": line.sale_order_line_id.price_subtotal
                                    * (line.warranty_config_id.percentage / 100),  
                        "warranty_id": line.sale_order_line_id.id,  
                        "sequence": line.sale_order_line_id.sequence,  
                    })

        res = self.env['sale.order.line'].create(new_order_line_list)
