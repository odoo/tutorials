from odoo import Command, models
from odoo.tools.float_utils import float_round


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_as_sold(self):
        for record in self:
            self.env['account.move'].create(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Down Payment",
                                "quantity": 1,
                                "price_unit": float_round(0.06 * record.selling_price, 2),
                            },
                        ),
                        Command.create(
                            {
                                "name": "Admin. Fees",
                                "quantity": 1,
                                "price_unit": 100,
                            },
                        ),
                    ],
                },
            )
        return super().action_mark_as_sold()
