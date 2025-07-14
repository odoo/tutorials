from odoo import models, Command
from odoo.exceptions import UserError, AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_state_sold(self):

        res = super().action_set_state_sold()
        journal = self.env["account.journal"].sudo().search([("type", "=", "sale")], limit=1)

        if not journal:
            raise UserError("No sales journal found!")

        try:
            self.check_access('write')
        except AccessError:
            raise UserError("You do not have sufficient access rights to create an invoice for this property.")

        for property in self:

            if property.buyer_id:
                commission = property.selling_price * 0.06
                admin_fee = 100.00
                self.env["account.move"].sudo().create(
                    {
                        "partner_id": property.buyer_id.id,
                        "move_type": "out_invoice",
                        "journal_id": journal.id,
                        "company_id": property.company_id.id,
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
