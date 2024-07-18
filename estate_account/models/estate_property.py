from odoo import Command, models


class estateproperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            record.check_access_rights('write')
            record.check_access_rule('write')
            self.env["account.move"].sudo().create(
                {
                    "move_type": "out_invoice",
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
                                "name": "administrative_fees",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )
        return super().action_sold()
