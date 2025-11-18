from odoo.exceptions import UserError

from odoo import models, Command


class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        for record in self:
            if record.selling_price == 0:
                raise UserError("Cannot sell Property without any accepted offer")
            self.env["account.move"].create(
                {
                    "partner_id": record.customer.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "6% of the selling price",
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "an additional 100.00 from administrative fees",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )
        return super().action_sold_property()
