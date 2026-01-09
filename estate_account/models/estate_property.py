from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_state_sold(self):
        res = super().action_state_sold()
        invoice_vals_list = []
        for record in self:
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "6% Commission",
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ],
                }
            invoice_vals_list.append(invoice_vals)
        self.env['account.move'].create(invoice_vals_list)
        return res
