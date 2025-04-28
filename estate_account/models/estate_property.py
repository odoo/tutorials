from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell(self):
        is_sold = super().action_sell()
        for record in self:
            self.env["account.move"].create({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        "name": "Down payment 6%",
                        "quantity": 1,
                        "price_unit": 0.06 * record.selling_price,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }),
                ],
            })
        return is_sold
