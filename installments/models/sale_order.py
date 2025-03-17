from odoo import models,fields, Command
from dateutil.relativedelta import relativedelta
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_emi = fields.Boolean(default=False)
    next_installment_date = fields.Date()
    installment_invoice_ids = fields.One2many('account.move', 'sale_order_id')

    def cron_recurring_create_installment_invoice(self):
        today = fields.Date.context_today(self)

        #for regular installments
        sale_orders = self.search([('is_emi', '=', True), ('next_installment_date', '=', today)])

        # Fetch the installment product
        installment_product = self.env.ref('installments.product_product_installment', False)
        if not installment_product:
            raise ValueError("Installment product with ID 'product_product_installment' is missing.")
        
        config = self.env['ir.config_parameter'].sudo()
        down_payment_percentage = float(config.get_param('installment.down_payment_percentage', default=0.0))
        annual_rate_percentage = float(config.get_param('installment.annual_rate_percentage', default=0.0))
        max_duration = float(config.get_param('installment.max_duration', default=12))
        admin_expenses_percentage = float(config.get_param('installment.admin_expenses_percentage', default=0.0))
        delay_penalty_process = float(config.get_param('installment.delay_penalty_days', 0.0))
        delay_penalty_percentage = float(config.get_param('installment.delay_penalty_percentage', default=0.0))

        for sale_order in sale_orders:

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
                'invoice_date_due': fields.Datetime.now() +relativedelta(month=1)   ,
                'invoice_line_ids': [
                    Command.create({
                        'product_id': installment_product.id,
                        'quantity': 1,
                        'price_unit': monthly_installment_amount,
                        'tax_ids': None,
                    })
                ],
                'sale_order_id': sale_order.id,
            }
            invoice = self.env['account.move'].create(invoice_vals)
            sale_order.installment_invoice_ids = [(4, invoice.id)]

            # Update the next installment date
            sale_order.next_installment_date = sale_order.next_installment_date + relativedelta(months=1) if sale_order.next_installment_date else today + relativedelta(months=1)

        #For penalty invoices
        delay_penalty_date = today - timedelta(days=delay_penalty_process)

        # Fetch the penalty product
        penalty_product = self.env.ref('installments.product_product_penalty', False)
        invoices = self.env["account.move"].search([
            ("move_type", "=", "out_invoice"),
            ("state", "=", "draft"),
            ('sale_order_id', "!=", False),
            ("penalty_applied", "=", False),
            ("invoice_date", "<=", delay_penalty_date),
        ])
        breakpoint()
        for invoice in invoices:
            #calculate penalty amount
            penalty_amount=(delay_penalty_percentage/100)*invoice.amount_total
            # Create the penalty invoice
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': invoice.partner_id.id,
                'invoice_date': today,
                'invoice_date_due': fields.Datetime.now() + relativedelta(month=1),
                'invoice_line_ids': [
                    Command.create({
                        'product_id': penalty_product.id,
                        'quantity': 1,
                        'price_unit': penalty_amount,
                        'tax_ids': None,
                    })
                ],
                'penalty_applied': True,
                'sale_order_id': invoice.sale_order_id.id,
            }
            penalty_invoice = self.env['account.move'].create(invoice_vals)

            invoice.write(
                        {
                            'penalty_applied': True,
                            'penalty_invoice_id':penalty_invoice.id
                        })
            


            

