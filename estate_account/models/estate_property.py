from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):

        res = super().action_sold_property()

        values_list = []
        for rec in self:
            values_list.append({
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
            })
        self.env['account.move'].create(values_list)

        return res
