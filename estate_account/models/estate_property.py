from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_state_sold(self):
        print("kjujhuh jnhjgiyi bh1")
        for record in self:
            self.env['account.move'].create(
                {
                    'partner_id': record.buyer_id.id,
                    'move_type': 'out_invoice',
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Selling Commission",
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100.00,
                            }
                        ),
                    ],
                }
            )
        print("kjujhuh jnhjgiyi bh2")
        return super().action_set_state_sold()
