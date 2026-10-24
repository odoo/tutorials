from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def action_sold_property(self):
        for rec in self:
            invoice_vals_list = {
                "partner_id": rec.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": f"{rec.name} - Down Payment",
                        "quantity": 1.0,
                        "price_unit": round(rec.selling_price * 0.06, 2)
                    }),
                    Command.create({
                        "name": f"{rec.name} - Administrative Fees",
                        "quantity": 1.0,
                        "price_unit": 100.0
                    }),
                ],
            }
            self.env['account.move'].create(invoice_vals_list)

        return super().action_sold_property()
