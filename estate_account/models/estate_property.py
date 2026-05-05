from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_state_to_sold(self):
        if not self.buyer_id:
            raise UserError("Properties can only be sold if the buyer is filled in")
        self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.buyer_id.id,
                "invoice_line_ids": [
                    Command.create({"name": "commission", "quantity": 1, "price_unit": self.selling_price * 0.06}),
                    Command.create({"name": "Administrative fee", "quantity": 1, "price_unit": 100}),
                ],
            }
        )
        return super().action_state_to_sold()
