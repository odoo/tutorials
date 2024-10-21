from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def action_set_sold_property(self):
        super().action_set_sold_property()

        values = {

            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {"name": "Commission Fee", "quantity": 1, "price_unit": 0.6 * self.selling_price + 100.00}
                ),
                Command.create(
                    {"name": "Administration Fee", "quantity": 1, "price_unit": 100.00}
                ),
            ],
        }

        accountMove = self.env["account.move"].create(values)
        return accountMove
        