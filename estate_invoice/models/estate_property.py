from odoo import Command, models


class EstateInvoiceModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        r = super().action_sold()

        self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': f'The property {self.name}',
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': f'Commission for property {self.name}',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100.0,
                })
            ]
        })

        return r
