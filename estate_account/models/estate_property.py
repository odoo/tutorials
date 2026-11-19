from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def action_sell_property(self):
        for record in self:
            self.env['account.move'].create({'partner_id': record.buyer_id.id,
                                            'move_type': 'out_invoice',
                                            'journal_id': 1,
                                            'invoice_line_ids': [
                                                Command.create({
                                                    "name": "Initial payment",
                                                    "quantity": 1,
                                                    "price_unit": 0.06 * record.expected_price
                                                }),
                                                Command.create({
                                                    "name": "Administration fees",
                                                    "quantity": 1,
                                                    "price_unit": 100
                                                })
                                            ],
                                            })
        # TODO - journal_id? I went in DEV mode to hardcode the sales journal, but how to find it from config?

        return super().action_sell_property()
