from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        self.ensure_one()
        invoice_values = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": "6% of property sale",
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06,
                    }
                ),
                Command.create(
                    {"name": "Admin fees", "quantity": 1, "price_unit": 100}
                ),
            ],
        }
        self.env["account.move"].create(invoice_values)

        return super().action_set_sold()
