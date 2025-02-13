from odoo import exceptions, Command, models
from odoo.exceptions import UserError


class Property(models.Model):
    _inherit="estate.property"

    def action_set_sold(self):

        invoice_vals = {
            "name": "Invoice Bill",
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "line_ids": [
                Command.create({
                    "name": "6% of the selling price",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                })
            ]
            }

        self.env["account.move"].create(invoice_vals)

        return super().action_set_sold()
