from odoo import models, Command


class InheritedProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        for record in self:
            self.env["account.move"].create({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": record.name + " Down Payment",
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }),
                ],
            })

        return super().sell_property()
