from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            invoice_lines = [
                Command.create(
                    {
                        "name": record.name + " (6% downpayment)",
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }
                ),
            ]

            invoice = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": invoice_lines,
            }
            self.env["account.move"].create(invoice)

        return super().action_sold()
