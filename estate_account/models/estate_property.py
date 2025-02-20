from odoo import Command, fields, models
from odoo.exceptions import UserError


class Property(models.Model):
    _inherit = "estate.property"

    journal_id = fields.Many2one(
        "account.journal",
        string="Invoicing Journal",
        store=True,
        domain=[("type", "=", "sale")],
    )

    def _get_default_journal(self):
        return self.env["account.journal"].search(
            [("type", "=", "sale")],
            limit=1,
        )

    def action_set_sold(self):
        if not self.journal_id:
            self.journal_id = self.__get_default_journal()
        if not self.journal_id:
            raise UserError("Please define an accounting sales journal.")
        move = self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "journal_id": self.journal_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": "Commission",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {"name": "Administrative fee", "quantity": 1, "price_unit": 100}
                    ),
                ],
            }
        )
        return super().action_set_sold()
