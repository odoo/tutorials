# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_ids = fields.One2many(comodel_name="account.move", inverse_name="property_id")

    def action_sell_property(self):
        super().action_sell_property()
        try:
            self.env["estate.property"].check_access("write")
        except:
            raise UserError("You do not have the necessary permissions to sell this property.")
        self.env["account.move"].sudo().create({
            "move_type": "out_invoice",
            "partner_id": self.buyer_id.id,
            "property_id": self.id,
            "line_ids": [
                Command.create({"name": self.name, "quantity": 1, "price_unit": 0.06 * self.selling_price}),
                Command.create({"name": "Administrative Fees", "quantity": 1, "price_unit": 100.0})
            ]
        })

    def action_view_invoice(self):
        if not self.invoice_ids:
            return
        action = {
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_id": self.invoice_ids.id,
        }
        return action
