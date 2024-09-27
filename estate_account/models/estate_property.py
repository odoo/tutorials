from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            values_property = {
                "partner_id": record.buyer_id.id,
                "name": record.name,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": record.name,
                            "quantity": 1,
                            "price_unit": 0.06 * record.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "administrative_fees",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }
        self.env["account.move"].create(values_property)
        return super().action_sold()
