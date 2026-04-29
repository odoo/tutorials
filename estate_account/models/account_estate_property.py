from odoo import Command, models


class AccountEstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):

        value = super().action_set_sold()

        self.env["account.move"].create(
            {
                "partner_id": self.salesman_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({"name": "Selling", "quantity": 1, "price_unit": self.selling_price * 0.6}),
                    Command.create({"name": "Admin fees", "quantity": 1, "price_unit": 100}),
                ],
            },
        )

        return value
