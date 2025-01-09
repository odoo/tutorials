from odoo import fields, models, Command
from dateutil.relativedelta import relativedelta
from datetime import timedelta

class InstallmentWizard(models.TransientModel):
    _name = 'installment.wizard'
    _description = 'Show installment information inside wizard'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    so_amount = fields.Float(readonly=True)
    down_payment = fields.Float(readonly=True)
    remaining_amount = fields.Float(readonly=True)
    interest = fields.Float(readonly=True)
    monthly_installment_count = fields.Float(readonly=True)
    monthly_installment_amount = fields.Float(readonly=True)
    is_emi = fields.Boolean(readonly=True)
    
    def default_get(self, fields):
        res = super().default_get(fields)
        
        active_id = self.env.context.get('active_id')  
        sale_order = self.env['sale.order'].browse(active_id)
         # Fetch default values based on the sale order and relevant calculations
        if sale_order:
            
            config = self.env['ir.config_parameter'].sudo()
            down_payment_percentage = float(config.get_param('installment.down_payment_percentage', default=0.0))
            annual_rate_percentage = float(config.get_param('installment.annual_rate_percentage', default=0.0))
            max_duration = float(config.get_param('installment.max_duration', default=1))  
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
            res['is_emi']=sale_order.is_emi
        return res

    def action_add_installment(self):
       today = fields.Date.context_today(self)
       for record in self:
        sale_order = record.sale_order_id
        if sale_order:
            sale_order.is_emi=True
       
            # Fetch default values based on the sale order and relevant calculations            
            config = self.env['ir.config_parameter'].sudo()
            down_payment_percentage = float(config.get_param('installment.down_payment_percentage', default=0.0))
            annual_rate_percentage = float(config.get_param('installment.annual_rate_percentage', default=0.0))
            max_duration = float(config.get_param('installment.max_duration', default=1))  
            admin_expenses_percentage = float(config.get_param('installment.admin_expenses_percentage', default=0.0))

            down_payment = (down_payment_percentage / 100) * sale_order.amount_total
            remaining_amount = sale_order.amount_total - down_payment
            admin_expenses = (admin_expenses_percentage / 100) * remaining_amount
            remaining_amount += admin_expenses
            interest = (remaining_amount * annual_rate_percentage*max_duration) / 100
            total_with_interest = remaining_amount + interest
            monthly_installment_count = max_duration*12
            monthly_installment_amount = total_with_interest / monthly_installment_count if monthly_installment_count else 0.0
            
            installment_product = self.env.ref('installments.product_product_installment')
            down_payment_product = self.env.ref('installments.product_product_down_payment')
            
             # Create the initial installment invoice
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': sale_order.partner_id.id,
                'invoice_date': today,
                'invoice_date_due': today + timedelta(days=30),
                'invoice_line_ids': [
                    Command.create({
                        'product_id': installment_product.id,
                        'quantity': 1,
                        'price_unit': monthly_installment_amount,
                        'tax_ids': None,
                    }),
                    Command.create({
                        'product_id': down_payment_product.id,
                        'quantity': 1,
                        'price_unit': down_payment,
                        'tax_ids': None,
                    })
                ],
                'sale_order_id': sale_order.id,
            }
            invoice = self.env['account.move'].create(invoice_vals)
            sale_order.installment_invoice_ids = [Command.link(invoice.id)]
            sale_order.next_installment_date=today + relativedelta(months=1)
