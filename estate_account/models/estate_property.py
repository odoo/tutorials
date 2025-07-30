from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = ["ninja.turtles.estate"]

    def action_mark_sold(self):
        res = super().action_mark_sold()

        for property in self:
            if not property.buyer_id:
                raise ValueError("Cannot create invoice without buyer.")

            invoice_vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": property.name,
                        "quantity": 1,
                        "price_unit": property.selling_price,
                    }),
                    Command.create({
                        "name": f"6%Commission for {property.name}",
                        "quantity": 1,
                        "price_unit": property.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }),
                ],
            }

            self.env["account.move"].create(invoice_vals)
        return res
