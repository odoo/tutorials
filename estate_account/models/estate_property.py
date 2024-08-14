from odoo import models, Command


class InheritedModel(models.Model):
    _inherit = "estate.property"

    def button_action_sold(self):
        result = super().button_action_sold()
        for record in self:
            commission = 0.06 * record.selling_price
            administrative_fee = 100
            invoice_vals = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": "6% Commission on Selling Price",
                            "price_unit": commission,
                        }
                    ),
                    Command.create(
                        {
                            "name": "administrative fees",
                            "price_unit": administrative_fee,
                        }
                    ),
                ],
            }
        self.env["account.move"].create(invoice_vals)
        return result
