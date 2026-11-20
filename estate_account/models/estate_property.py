from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def action_sell_property(self):
        for record in self:
            account_journal = record.env['account.journal'].search([('name', '=', 'Sales')])
            self.env['account.move'].create({'partner_id': record.buyer_id.id,
                                            'move_type': 'out_invoice',
                                            'journal_id': account_journal.id,
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
        return super().action_sell_property()
