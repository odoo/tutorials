from odoo import models, Command


class EstateAccount(models.Model):
    _inherit = "public.property"
    def action_sold(self):
        fees = 0.06 * self.selling_price
        print(" reached ".center(100, '='))
        self.check_access('write')
        account_move = self.env["account.move"].sudo().create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": "6% of the selling price",
                            "quantity": 1,
                            "price_unit": fees,
                        }
                    ),
                    Command.create(
                        {
                            "name": "100 rupees administrative fee",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }
        )
        return super().action_sold()
