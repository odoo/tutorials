from odoo import Command, _, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        res = super().action_set_sold()

        for property in self:
            if not property.buyer_id:
                continue

            commission = property.selling_price * 0.06
            admin_fee = 100.00

            invoice_vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": _("6% Commission"),
                            "quantity": 1,
                            "price_unit": commission,
                        }
                    ),
                    Command.create(
                        {
                            "name": _("Administrative Fees"),
                            "quantity": 1,
                            "price_unit": admin_fee,
                        }
                    ),
                ],
            }

            invoice = self.env["account.move"].create(invoice_vals)

        return res
