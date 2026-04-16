from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        super().action_sold()
        for record in self:
            self.env['account.move'].create({
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
