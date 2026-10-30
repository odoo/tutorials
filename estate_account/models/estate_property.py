from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        res = super().action_sell_property()
        self.env['account.move'].create([
            {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({"name": property.name, "quantity": 1, "price_unit": property.selling_price * 0.06}),
                    Command.create({"name": "admin fee", "quantity": 1, "price_unit": 100.00}),
                ],
            }
            for property in self
        ])
        return res
