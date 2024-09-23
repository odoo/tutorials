from odoo import models, fields
from datetime import timedelta, datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    installement_amount = fields.Integer(string="Installment Amount")
    is_installable = fields.Boolean(default=False)

    def schedule_penalty_invoices(self):

        unpaid_orders = self.search([('is_installable', '!=', False)])

        for order in unpaid_orders:
            penalty_percentage = self.env['ir.config_parameter'].get_param(
                'installement.delay_penalty_percentage', default=0)

            penalty_days = int(self.env['ir.config_parameter'].get_param(
                'installement.delay_penalty_process', default=0))

            last_payment_date = max(order.invoice_ids.mapped(
                'invoice_date')) if order.invoice_ids else order.date_order.date()

            if datetime.now().date() > last_payment_date + timedelta(days=penalty_days):

                penalty_amount = int(order.installement_amount * int(penalty_percentage)) / 100

                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': order.partner_id.id,
                    'invoice_line_ids': [(0, 0, {
                        'product_id': self.env.ref('installement.monthly_emi_product').id,
                        'quantity': 1,
                        'price_unit': penalty_amount,
                        'sale_line_ids': [(fields.Command.set(order.order_line.mapped('id')))]
                    })],
                    'invoice_date': fields.Date.today(),
                })
                invoice.action_post()

    def document_upload_installement(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "documents.document_action")
        return action
