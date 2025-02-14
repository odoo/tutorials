# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        if not self.buyer_id.id:
            raise UserError("No buyer set for this property.")

        try:
            self.check_access_rights("write", raise_exception=True)
            self.check_access_rule("write")
        except AccessError:
            raise UserError("You do not have the required permissions to update this property.")

        self.env["account.move"].sudo().create({
            "move_type": "out_invoice",
            "partner_id": self.buyer_id.id,
            "line_ids": [
                Command.create({"name": self.name, "quantity": 1, "price_unit": 0.06 * self.selling_price}),
                Command.create({"name": "Administrative Fees", "quantity": 1, "price_unit": 100.0})
            ]
        })

        return super().action_sell_property()
