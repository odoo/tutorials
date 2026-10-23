from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def property_sold(self):
        for record in self:
            self.env["account.move"].create({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": 0.06 * record.selling_price,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }),
                ],
            })
        return super().property_sold()
