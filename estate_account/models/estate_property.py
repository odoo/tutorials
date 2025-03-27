from odoo import api, fields, models, Command


class Property(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        res = super().action_set_sold()

        for record in self:
            record.check_access('create')
            invoice_line_ids = [
                Command.create({
                    'name': record.name,
                    'quantity': 1,
                    'price_unit': record.selling_price * 0.06
                }),
                Command.create({
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 100
                })
            ]

            moves = record.env['account.move'].sudo().with_context(default_move_type='out_invoice').create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': invoice_line_ids
            })
        return res
