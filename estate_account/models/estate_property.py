from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        invoice_vals_list = []

        for prop in self:
            invoice_vals_list.append(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "6% of selling price",
                                "quantity": 1,
                                "price_unit": prop.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1,
                                "price_unit": 1000,
                            }
                        ),
                    ],
                }
            )

        if invoice_vals_list:
            self.env["account.move"].create(invoice_vals_list)
        return res
