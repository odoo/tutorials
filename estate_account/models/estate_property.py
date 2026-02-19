from odoo import models, Command

class EstatePropertyInherited(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super(EstatePropertyInherited, self).action_sold()

        for offer in self:
            if not offer.buyer_id or not offer.selling_price:
                continue

            invoice_vals = {
                "partner_id": offer.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Commission (6%) for {offer.name}",
                        "quantity": 1,
                        "price_unit": offer.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ],
            }

            invoice = self.env["account.move"].create(invoice_vals)
            print(f"Invoice created: {invoice.name}")

        return res
