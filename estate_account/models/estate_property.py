from odoo import Command, models


class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        for record in self:
            res = super().action_property_sold()
            self.env["account.move"].sudo().create(
                {
                    "partner_id": record.buyer_id.partner_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create({
                            "name": "six percent charge",
                            "quantity": "1",
                            "price_unit": record.selling_price * 0.06,
                        }),
                        Command.create({
                            "name": "administration fee",
                            "quantity": "1",
                            "price_unit": 100.0,
                        }),
                    ],
                },
            )
        return res
