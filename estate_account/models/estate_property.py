from odoo import models, Command, fields


class EstateProperty(models.Model):
    _inherit = ['estate.property']
    _name = 'estate.property'

    invoice_count = fields.Integer(compute='_compute_invoice_count', string="Invoice Count")

    def action_mark_as_sold(self):
        # Keep it at the beginning to trigger the validation first
        result = super().action_mark_as_sold()

        for record in self:
            # It's valid to assume that there is one accepted offer (validated by the inherited entity)
            accepted_offer = record.offer_ids.filtered(lambda offer: offer.status == 'accepted')[0]

            account_move = self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "6% of selling price",
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ],
            })

            accepted_offer.account_move_id = account_move

        return result

    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.offer_ids.account_move_id)

    def action_view_invoices(self):
        self.ensure_one()
        invoices = self.offer_ids.account_move_id
        return invoices._get_records_action()
