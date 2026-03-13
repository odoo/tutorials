from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            commission_amount = record.selling_price * 0.06
            invoice_vals = {
                "move_type": "out_invoice",
                "partner_id": record.buyer_id.id,
                "invoice_origin": record.name,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "6% Commission",
                            "quantity": 1,
                            "price_unit": commission_amount,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.0,
                        }
                    ),
                ],
            }
            self.env["account.move"].with_context(
                default_move_type="out_invoice"
            ).create(invoice_vals)
        return super().action_sold()
