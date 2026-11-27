from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):

        res = super().action_set_sold()

        account_journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        account_journal.ensure_one()
        vals_list = []

        for record in self:
            if not record.buyer_id:
                raise UserError(self.env._("Cannot create an invoice without a buyer"))
            vals = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": account_journal.id,
                "line_ids": [
                    Command.create(
                        {
                            "name": self.env._("6%% of %s price", record.name),
                            "quantity": 1,
                            "price_unit": record.selling_price * 0.06,
                        },
                    ),
                    Command.create(
                        {
                            "name": self.env._("Administrative fees"),
                            "quantity": 1,
                            "price_unit": 100.00,
                        },
                    ),
                ],
            }
            vals_list.append(vals)

        self.env["account.move"].create(vals_list)

        return res
