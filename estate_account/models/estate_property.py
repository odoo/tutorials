from odoo import fields, Command, models
import base64

class EstateProperty(models.Model):
    _inherit = 'estate.property'
    _description = 'Inherited estate property model'

    def action_set_sold(self):
        for record in self:
            record.check_access('create')
            invoice_vals = {
                        'move_type': 'out_invoice',  
                        'partner_id': record.partner_id.id,  
                        'invoice_date': fields.Date.today(),  
                        'invoice_line_ids': [
                            Command.create(
                                {
                                    "name": record.display_name,
                                    "quantity": 1,
                                    "price_unit": record.selling_price
                                }
                            ),
                            Command.create(
                                {
                                    "name": '"6%" of Property Sale Price',
                                    "quantity": 1,
                                    "price_unit": record.selling_price * 0.06,
                                }
                            ),
                            Command.create(
                                {
                                    "name": "Administrative Fees",
                                    "quantity": 1,
                                    "price_unit": 100,
                                }
                            ),
                        ],
                    }

            invoice = self.env["account.move"].sudo().create(invoice_vals)
            pdf_data = self.env['ir.actions.report']._render('account.report_invoice', invoice.id)[0]
            attachment = self.env['ir.attachment'].create({
                'name': f'Invoice {invoice.name}.pdf',
                'type': 'binary',
                'datas': base64.b64encode(pdf_data),
                'res_model': 'account.move',
                'res_id': invoice.id,
            })
            mail_template = self.env.ref('estate.property_sold_email_template')
            mail_values = {
                'attachment_ids': [(6, 0, [attachment.id])],  
            }
            mail_template.send_mail(record.id, force_send=True, email_values=mail_values)

        return super().action_set_sold()
