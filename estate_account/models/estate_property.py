from odoo import Command, api, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for record in self:
            # Create the account move for each record
            record.check_access('create')
            print(" reached ".center(100, '='))
            move = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.buyer_id.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100,
                    })
                ],
                'name': record.estate_property_seq,
            })
        return super().action_sold()
