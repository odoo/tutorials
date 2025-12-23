from odoo import Command, models


class Property(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        res = super().action_sell_property()

        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        "name": f"6% pre-payement for {record.name}",
                        "quantity": 1.0,
                        "price_unit": 0.06 * record.selling_price,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.00,
                    }),
                ],
            })
        return res
