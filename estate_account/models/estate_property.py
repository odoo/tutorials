from odoo import api, Command, fields, models
from odoo.exceptions import UserError


class estateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        result = super().action_sold()
        invoice = self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": self.env["account.journal"]
                .search([("type", "=", "sale")], limit=1)
                .id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Property Sale Commision",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
        )
        return result
