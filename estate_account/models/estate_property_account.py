# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models
from odoo.exceptions import AccessError, UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.ensure_one()
        try:
            self.check_access("write")
        except AccessError:
                raise UserError(f"You do not have write access to sell the property '{self.name}'.")

        invoice_lines = [
            Command.create({
            "name": f"self: {self.name}",
            "quantity": 1,
            "price_unit": self.selling_price,
                }
            ),
            Command.create(
                {
                    "name": "6% Commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }
            ),
            Command.create(
                {
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                }
            ),
            Command.create(
                {
                    "name": "Discount",
                    "quantity": 1,
                    "price_unit": -self.selling_price * 0.05,
                }
            ),
        ]
        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": invoice_lines,
            "invoice_origin": f"self: {self.name}",
            "narration": f"Invoice related to self '{self.name}'",
        }
        self.env["account.move"].sudo().create(invoice_vals)
        return super().action_sold()
