# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, Command, api
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        try:
            self.check_access("write") 
        except AccessError:
            raise ValidationError("You do not have permission to sell this property.")

        if not self.buyer_id:
            raise ValidationError("Cannot create invoice without a buyer.")

        invoice = self.sudo().env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({"name": "Property Selling Fee", "quantity": 1, "price_unit": self.selling_price * 0.06,}),
                    Command.create({"name": "Administrative Fees", "quantity": 1, "price_unit": 100.00,}),
                ],
            }
        )

        return super(EstateProperty, self).action_sold()
