from odoo import models,fields, Command
from dateutil.relativedelta import relativedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_emi = fields.Boolean(default=False)
    next_installment_date = fields.Date()
    installment_invoice_ids = fields.One2many('account.move', 'sale_order_id')

    def cron_recurring_create_installment_invoice(self):
        today = fields.Date.context_today(self)
        sale_orders = self.search([('is_emi', '=', True), ('next_installment_date', '=', today)])

        # Fetch the installment product
        installment_product = self.env.ref('installments.product_product_installment', False)
        if not installment_product:
            raise ValueError("Installment product with ID 'product_product_installment' is missing.")
        
        for sale_order in sale_orders:
            config = self.env['ir.config_parameter'].sudo()
            down_payment_percentage = float(config.get_param('installment.down_payment_percentage', default=0.0))
            annual_rate_percentage = float(config.get_param('installment.annual_rate_percentage', default=0.0))
            max_duration = float(config.get_param('installment.max_duration', default=12))
            admin_expenses_percentage = float(config.get_param('installment.admin_expenses_percentage', default=0.0))

            # Calculate financial values
            down_payment = (down_payment_percentage / 100) * sale_order.amount_total
            remaining_amount = sale_order.amount_total - down_payment
            admin_expenses = (admin_expenses_percentage / 100) * remaining_amount
            remaining_amount += admin_expenses
            interest = (remaining_amount * annual_rate_percentage * max_duration) / 100
            total_with_interest = remaining_amount + interest
            monthly_installment_count = max_duration * 12
            monthly_installment_amount = total_with_interest / monthly_installment_count if monthly_installment_count else 0.0

            # Check if there are already 24 invoices
            if len(sale_order.installment_invoice_ids) >= 24:
                sale_order.next_installment_date = False
                continue
         
            # Create the installment invoice
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': sale_order.partner_id.id,
                'invoice_date': today,
                'invoice_payment_term_id': 'account.account_payment_term_end_following_month',
                'invoice_line_ids': [
                    Command.create({
                        'product_id': installment_product.id,
                        'quantity': 1,
                        'price_unit': monthly_installment_amount,
                    })
                ],
                'sale_order_id': sale_order.id,
            }
            invoice = self.env['account.move'].create(invoice_vals)
            sale_order.installment_invoice_ids = [(4, invoice.id)]

            # Update the next installment date
            sale_order.next_installment_date = sale_order.next_installment_date + relativedelta(months=1) if sale_order.next_installment_date else today + relativedelta(months=1)
