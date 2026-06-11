from markupsafe import Markup
from odoo import _, models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self, open_wizard=True):
        super().action_sold()
        for record in self:
            record.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': f'property {record.name}',
                        'quantity': 1,
                        'price_unit': record.selling_price,
                    }),
                    Command.create({
                        'name': f'6% commission on {record.name}',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': f'Administrative fees on {record.name}',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            })
            if open_wizard:
                ctx = {
                    'default_partner_ids': [record.buyer_id.id],
                    'default_subject': f'Property {record.name} has been sold',
                    'default_body': (
                        f'<p>Dear {record.buyer_id.name},</p>'
                        f'<p>We are pleased to inform you that the purchase of the property '
                        f'<b>{record.name}</b> has been successfully completed.</p>'
                        f'<p>The agreed selling price of <b>${record.selling_price:,.2f}</b> '
                        f'has been recorded, and an invoice has been issued for your reference. '
                        f'Please review the attached invoice for the full breakdown, including '
                        f'the 6% agency commission and administrative fees.</p>'
                        f'<p>Should you have any questions or require further assistance, '
                        f'do not hesitate to reach out to us.</p>'
                        f'<p>Thank you for choosing our services. We wish you all the best '
                        f'in your new property.</p>'
                        f'<p>Warm regards,<br/>The Real Estate Team</p>'
                    ),
                }
                return {
                    'name': _('Send Email'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'mail.compose.message',
                    'target': 'new',
                    'context': ctx,
                }
            else:
                record.message_post(
                    subject=f'Property {record.name} has been sold',
                    partner_ids=[record.buyer_id.id],
                    body=Markup(
                        f'<p>Dear {record.buyer_id.name},</p>'
                        f'<p>We are pleased to inform you that the purchase of the property '
                        f'<b>{record.name}</b> has been successfully completed.</p>'
                        f'<p>The agreed selling price of <b>${record.selling_price:,.2f}</b> '
                        f'has been recorded, and an invoice has been issued for your reference. '
                        f'Please review the attached invoice for the full breakdown, including '
                        f'the 6% agency commission and administrative fees.</p>'
                        f'<p>Should you have any questions or require further assistance, '
                        f'do not hesitate to reach out to us.</p>'
                        f'<p>Thank you for choosing our services. We wish you all the best '
                        f'in your new property.</p>'
                        f'<p>Warm regards,<br/>The Real Estate Team</p>'
                    ),
                    message_type='email',
                )
