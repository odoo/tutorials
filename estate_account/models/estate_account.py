from odoo import models
from odoo.exceptions import UserError
from odoo.orm.commands import Command


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        for order in self:
            selling_price, buyer_id = max(
                (
                    (x.price, x.partner_id)
                    for x in order.offer_ids
                    if x.status != "refused"
                ),
                default=(None, None),
                key=lambda x: x[0],
            )

            if not buyer_id or not selling_price:
                raise UserError("You cannot sell without a buyer")

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
