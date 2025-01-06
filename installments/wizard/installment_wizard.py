from odoo import api, fields, models

class InstallmentWizard(models.TransientModel):
    _name = 'installment.wizard'
    _description = 'Show installment information inside wizard'

    sale_order_id= fields.Many2one('sale.order', string="Sale Order")
    so_amount=fields.Float(readonly=True)
    down_payment=fields.Float(readonly=True)
    remaining_amount=fields.Float(readonly=True)
    interest=fields.Float(readonly=True)
    monthly_installment_count=fields.Float(readonly=True)
    monthly_installment_amount=fields.Float(readonly=True)
    
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get('active_id')  
        sale_order = self.env['sale.order'].browse(active_id)
         # Fetch default values based on the sale order and relevant logic
        if sale_order:
            config = self.env['ir.config_parameter'].sudo()
            down_payment_percentage = float(config.get_param('installment.down_payment_percentage', default=0.0))
            annual_rate_percentage = float(config.get_param('installment.annual_rate_percentage', default=0.0))
            max_duration = float(config.get_param('installment.max_duration', default=12))  # Default to 12 months
            admin_expenses_percentage = float(config.get_param('installment.admin_expenses_percentage', default=0.0))

            down_payment = (down_payment_percentage / 100) * sale_order.amount_total
            remaining_amount = sale_order.amount_total - down_payment
            admin_expenses = (admin_expenses_percentage / 100) * remaining_amount
            remaining_amount += admin_expenses
            interest = (remaining_amount * annual_rate_percentage*max_duration) / 100
            total_with_interest = remaining_amount + interest
            monthly_installment_count = max_duration*12
            monthly_installment_amount = total_with_interest / monthly_installment_count if monthly_installment_count else 0.0

            # Assign computed values to the fields
            res['sale_order_id'] = sale_order.id
            res['so_amount'] = sale_order.amount_total
            res['down_payment'] = down_payment
            res['remaining_amount'] = remaining_amount
            res['interest'] = interest
            res['monthly_installment_count'] = monthly_installment_count
            res['monthly_installment_amount'] = monthly_installment_amount
            breakpoint()
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
                        "name": f"{line.warranty_config_id.name}",
                        "product_id": line.warranty_config_id.warranty_product.product_variant_id.id,  
                        "price_unit": line.sale_order_line_id.price_subtotal
                                    * (line.warranty_config_id.percentage / 100),  
                        "linked_line_id": line.sale_order_line_id.id,
                        "sequence": line.sale_order_line_id.sequence,  
                    })

        self.env['sale.order.line'].create(warranty_product_list)
