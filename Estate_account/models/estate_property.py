from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for property in self:
            invoice_vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": "Commission (6%)",
                        "quantity": 1,
                        "price_unit": property.selling_price * 0.06,
                    }),

                    Command.create({
                        "name": "Administrative Fee",
                        "quantity": 1,
                        "price_unit": 100,
                    }),
                ],
            }
            self.env["account.move"].create(invoice_vals)

        return super().action_set_sold()
