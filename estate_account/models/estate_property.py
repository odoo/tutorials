from odoo import models,Command

class EstateProperty(models.Model):
    _description = "Estate Account property Model"
    _inherit="estate.property"

    def action_mark_property_sold(self):
        # print(" reached ".center(100, '='))
        self.check_access('write')

        self.env["account.move"].sudo().create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price,
                }),
                Command.create({
                    "name": "Property Sale Commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Additional Fees",
                    "quantity": 1,
                    "price_unit": 100.00
                })
            ],
        })
        return super().action_mark_property_sold()
