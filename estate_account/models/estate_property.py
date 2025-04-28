from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        invoice_vals_list = []
        purchase_journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for record in self:
            invoice_vals = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": purchase_journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "[SO] 6%",
                            "quantity": 1,
                            "price_unit": record.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "[SO] Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.0,
                        }
                    ),
                ],
            }
            invoice_vals_list.append(invoice_vals)
        self.env["account.move"].create(invoice_vals_list)
        return super().action_sold_property()
