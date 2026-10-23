from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_estate_property(self):
        print("action_sold_estate_property")
        invoice = self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [(0, 0, {
                "name": "Sell of '" + self.name + "'",
                "quantity": 1,
                "price_unit": 0.06 * self.selling_price,
            }), (0, 0, {
                "name": "administrative fees",
                "quantity": 1,
                "price_unit": 100.00,

            })]
        })
        return super().action_sold_estate_property()
