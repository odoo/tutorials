from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        res = super().action_sold()

        for record in self:
            buyer = record.buyer_id or record.salesperson_id or self.env.user.partner_id

            invoice = self.env["account.move"].create({
                "partner_id": buyer.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": record.name,
                        "quantity": 1.0,
                        "price_unit": record.selling_price,
                    }),
                    Command.create({
                        "name": f"6% Selling Commission Fee for {record.name}",
                        "quantity": 1.0,
                        "price_unit": record.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative Processing Fees",
                        "quantity": 1.0,
                        "price_unit": 100.00,
                    }),
                ],
            })

            invoice._compute_amount()

        return res
