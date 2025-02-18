# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, Command
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        try:
            self.check_access("write")
        except AccessError:
            raise ValidationError("You do not have the required permissions to update this property.")
        if not self.buyer_id.id:
            raise ValidationError("No buyer set for this property.")

        self.env["account.move"].sudo().create({
            "move_type": "out_invoice",
            "partner_id": self.buyer_id.id,
            "line_ids": [
                Command.create({"name": self.name, "quantity": 1, "price_unit": 0.06 * self.selling_price}),
                Command.create({"name": "Administrative Fees", "quantity": 1, "price_unit": 100.0})
            ]
        })

        return super().action_sell_property()
