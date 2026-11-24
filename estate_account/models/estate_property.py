from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        result = super().action_sold()

        for property_record in self:
            if not property_record.buyer_id:
                raise UserError(
                    "Please select a buyer before selling."
                )

            journal = self.env["account.journal"].search([
                ("type", "=", "sale"),
                ("company_id", "=", self.env.company.id),
            ], limit=1)

            if not journal:
                raise UserError(

                    "No sales journal is configured."
                )

            self.env["account.move"].create({
                "partner_id": property_record.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Property Sale - {property_record.name}",
                        "quantity": 1,
                        "price_unit": property_record.selling_price,
                    }),
                    Command.create({
                        "name": "Property Sales Commission",
                        "quantity": 1,
                        "price_unit":
                            property_record.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ],
            })

        return result
