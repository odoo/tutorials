from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate_property"

    def mark_as_sold(self):
        account_move = self.env['account.move']
        for values in self:
            account_values = {
                'partner_id': values.buyer_id.id,
                'move_type': 'out_invoice',
                "line_ids": [
                    Command.create({
                        "name": "6% commission",
                        "quantity": "1",
                        "price_unit": values.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "administrative fees",
                        "quantity": "1",
                        "price_unit": 100,
                    })
                ],
            }

            account_move.sudo().create(account_values)

        return super().mark_as_sold()
