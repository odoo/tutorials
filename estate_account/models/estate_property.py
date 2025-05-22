from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_listing(self):
        self._create_empty_account_move()
        return super().action_sell_listing()

    def _create_empty_account_move(self):
        for property in self:
            self.env["account.move"].create({
                "partner_id": property.partner_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        'name': f' 6 % Downpayment for {property.name} (total price: {property.selling_price})',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Admin Fees",
                        'quantity': 1,
                        'price_unit': 100,
                    })
                ],
            })
