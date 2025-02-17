from odoo import models, Command, fields


class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.ensure_one()
        self.check_access('write')

        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "property_id": self.id,
            "line_ids": [
                (
                    Command.create({
                        "name": "6% of selling price",
                        "quantity": 1,
                        "price_unit": (self.selling_price * 0.06)
                    })
                ),
                (
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00
                    })
                )
            ]
        }

        print(" reached ".center(100, '='))

        self.env["account.move"].sudo().create(invoice_vals)
        return super().action_sold()
