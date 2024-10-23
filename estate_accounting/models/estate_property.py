from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_estate_property_sold(self):
        for record in self:
            account_move_params = {
                "partner_id": record.buyer.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": record.name,
                        "quantity": "1",
                        "price_unit": record.selling_price
                    }),
                    Command.create({
                        "name": "6% Additional",
                        "quantity": "1",
                        "price_unit": record.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": "1",
                        "price_unit": "100"
                    })
                ]
            }

            self.env['account.move'].create(account_move_params)

            return super().action_estate_property_sold()
