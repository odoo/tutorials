from odoo import Command, models
from odoo.exceptions import UserError

COMMISSION_RATE = 0.06
ADMINISTRATIVE_FEE = 100.00


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        invoice_list = []
        for record in self:
            if not record.buyer_id:
                raise UserError(
                    self.env._(
                        "A buyer must be set before creating an invoice for a sold property."
                    )
                )
            invoice = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": record.name,
                            "quantity": 1,
                            "price_unit": record.selling_price * COMMISSION_RATE,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": ADMINISTRATIVE_FEE,
                        }
                    ),
                ],
            }
            invoice_list.append(invoice)

        self.env["account.move"].create(invoice_list)
        return res
