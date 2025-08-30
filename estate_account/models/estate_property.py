from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_property_as_sold(self):
        result_super = super().action_mark_property_as_sold()

        for record in self:
            accepted_offer = self.env["estate.property.offer"].search_fetch(
                [("property_id", "=", record.id), ("status", "=", "accepted")], ["partner_id"], limit=1
            )
            self.env["account.move"].create(
                {
                    "partner_id": accepted_offer.partner_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create({"name": record.name, "quantity": 1, "price_unit": accepted_offer.price}),
                        Command.create(
                            {"name": "6% Commision", "quantity": 1, "price_unit": accepted_offer.price * (0.6)}
                        ),
                        Command.create({"name": "Administrative fees", "quantity": 1, "price_unit": 100.00}),
                    ],
                }
            )

        return result_super
