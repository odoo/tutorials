from odoo import models, exceptions, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_sold(self):
        if not self.buyer_id:
            raise exceptions.UserError("A buyer is needed to sell a property")

        self.env['account.move'].with_context(default_move_type='out_invoice').create(
            {
            "partner_id": self.buyer_id.id,
            "invoice_line_ids": [
            Command.create({
                "name": "Price Percentage",
                "quantity": 1,
                "price_unit": self.selling_price * 6 / 100,
            }),
            Command.create({
                "name": "Administrative Fees",
                "quantity": 1,
                "price_unit": 100.00,
            })
        ]
        })

        return super().set_sold()
