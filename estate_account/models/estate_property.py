from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()

        for record in self:
            if record.buyer_id:
                invoice_vals = {
                    "partner_id": record.buyer_id.id,
                    "estate_property_id": record.id,
                    "estate_property_tag_id": record.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Property commission (6%)",
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
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
                self.env["account.move"].create(invoice_vals)

        return res
