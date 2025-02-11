from odoo import Command, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        if not self.buyer_id.id:
            raise UserError("Property without buyer cannot be sold")

        self.env["estate.property"].check_access("write")

        self.sudo().env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.buyer_id.id,
            "line_ids": [
                Command.create({"name": self.name, "quantity": 1, "price_unit": 0.06 * self.selling_price}),
                Command.create({"name": "Administrative Fees", "quantity": 1, "price_unit": 100.0})
            ]
        })
        return super().action_sold()
