from odoo import Command, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["estate.property"]

    def action_sold(self):
        for record in self:
            self.env["account.move"].with_context(default_move_type="out_invoice").create(
                {
                    "partner_id": record.buyer_id.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "quantity": 1,
                                "price_unit": 0.06 * record.selling_price,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1,
                                "price_unit": 100000,
                            }
                        ),
                    ],
                }
            )
        return super().action_sold()
