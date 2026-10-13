from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for record in self:
            record.state = 'sold'
            self.env["account.move"].create(
                {
                    'partner_id': record.buyer.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            'name': '6% Commission',
                            'quantity': 1,
                            'price_unit': record.selling_price * 0.06
                        }),
                        Command.create({
                            'name': 'Administrative fees',
                            'quantity': 1,
                            'price_unit': 100.00,
                        })
                    ]
                }
            )
        return super().action_sold()
