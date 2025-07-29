from odoo import models, fields

"""
NOTE
An account move is just a group of operations (account move lines)
E.g.: a vendor bill is an account move
      a customer invoice is an account move too
"""


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self) -> bool:
        if not super().action_sell_property():
            return False
        record: EstateProperty
        for record in self:
            partner_id: int = record.buyer_id.id
            invoice_lines = [
                fields.Command.create(
                    {
                        "name": "Partial pay",
                        "quantity": 1,
                        "price_unit": record.selling_price / 100 * 6
                    }
                ),
                fields.Command.create(
                    {
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100
                     }
                ),
            ]
            account_move = self.env["account.move"].create(
                {
                    "move_type": "out_invoice",
                    "partner_id": partner_id,
                    "invoice_line_ids": invoice_lines
                }
            )
