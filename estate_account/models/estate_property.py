from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        for record in self:
            record.env["account.move"].create(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create({
                            "name": "6% of the selling price",
                            "price_unit": record.selling_price * 0.06,
                            "quantity": 1,
                        }),
                        Command.create({
                            "name": "Administration Fee",
                            "price_unit": 20,
                            "quantity": 1,
                        })
                    ]
                },
            )

        return super().action_sell_property()
