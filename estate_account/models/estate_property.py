from odoo import models, Command


class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        for record in self:
            commission_amount = record.selling_price * 0.06
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    # Line 1: 6% Commission
                    Command.create({
                        "name": f"6% Commission for {record.name}",
                        "quantity": 1.0,
                        "price_unit": commission_amount,
                    }),
                    # Line 2: Administrative Fees
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1.0,
                        "price_unit": 100.0,
                    }),
                ],
            })

        return res
