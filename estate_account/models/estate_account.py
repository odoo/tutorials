from odoo import models
from odoo.exceptions import UserError
from odoo.orm.commands import Command


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        for order in self:
            best_offer = order.offer_ids.filtered(lambda x: x.status == "accepted").sorted("price DESC")[:1]

            if not best_offer:
                raise UserError("You cannot sell without an accepted offer")

            buyer_id = best_offer[0].buyer_id
            selling_price = best_offer[0].selling_price

            invoice_vals = {
                "move_type": "out_invoice",
                "partner_id": buyer_id.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Down Payment (6% of the selling price)",
                            "quantity": 1,
                            "price_unit": 0.06 * selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }

            self.env["account.move"].create(invoice_vals)

        return super().sold_action()
