from odoo.exceptions import AccessError

from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def action_set_sold_property(self):
        super().action_set_sold_property()

        # print(" reached ".center(100, '='))

        try:
            self.check_access_rights('write')
            self.check_access_rule('write')
        except AccessError:
            raise AccessError("You do not have permission to update this property.")

        values = {

            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {"name": "Commission Fee", "quantity": 1, "price_unit": 0.6 * self.selling_price + 100.00}
                ),
                Command.create(
                    {"name": "Administration Fee", "quantity": 1, "price_unit": 100.00}
                ),
            ],
        }

        accountMove = self.env["account.move"].sudo().create(values)
        return accountMove
