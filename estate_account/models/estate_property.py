from odoo import models, exceptions, Command


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        for record in self:
            if not record.buyer_id:
                raise exceptions.UserError("Can't sell a property without a buyer.")
            record.check_access('write')
            record.env["account.move"].sudo().create({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                Command.create({
                    "name": "Price Percentage",
                    "quantity": 1,
                    "price_unit": record.selling_price * 6 / 100,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                })
            ]
            })

        return super().sell_property()
