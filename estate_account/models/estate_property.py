from odoo import models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        res = super().action_property_sold()
        for property in self:
            if not property.buyer_id:
                continue

            journal = self.env["account.journal"].search(
                [("type", "=", "sale")], limit=1
            )

            if not journal:
                raise UserError("No sales journal found!")

            commission = property.selling_price * 0.06

            admin_fee = 100.00

            self.env["account.move"].create(
                {
                    "partner_id": property.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Commission (6%)",
                                "quantity": 1,
                                "price_unit": commission,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1,
                                "price_unit": admin_fee,
                            }
                        ),
                    ],
                }
            )
        return res
