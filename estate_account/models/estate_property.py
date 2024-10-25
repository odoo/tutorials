from odoo import Command, models


class Property(models.Model):
    _inherit = ["estate.property"]

    def action_sell(self):
        offer_id = self.offer_ids.search([("is_accepted", "=", True)], limit=1)
        self.env["account.move"].create(
            {
                "name": "c_est_l_heure_de_payer",
                "partner_id": offer_id.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": self.address,
                        "quantity": 1,
                        "price_unit": offer_id.amount
                    })
                ],
            }
        )
        return super().action_sell()
