from odoo import Command, _, models
from odoo.exceptions import MissingError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        if not journal:
            raise MissingError(_("Missing sales journal."))
        invoice_vals_list = []
        for estate in self:
            invoice_vals = {
                "move_type": "out_invoice",
                "invoice_user_id": estate.salesman_id.id,
                "partner_id": estate.buyer_id.id,
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": estate.name,
                            "quantity": 1,
                            "price_unit": estate.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.0,
                        }
                    ),
                ],
            }
            invoice_vals_list.append(invoice_vals)
        self.env["account.move"].create(invoice_vals_list)
        return super().action_sold()
