# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        super().action_sell_property()
        try:
            self.env["estate.property"].check_access("write")
        except:
            raise UserError("You do not have the necessary permissions to sell this property.")
        self.sudo().env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.buyer_id.id,
            "line_ids": [
                Command.create({"name": self.name, "quantity": 1, "price_unit": 0.06 * self.selling_price}),
                Command.create({"name": "Administrative Fees", "quantity": 1, "price_unit": 100.0})
            ]
        })
