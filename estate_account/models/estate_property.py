# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import models, Command, fields, _
from odoo.exceptions import AccessError

class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        try:
            self.ensure_one()
            self.check_access('write') 
        except AccessError:
            raise AccessError(_("You do not have the permission to mark this property as sold."))

        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "property_id": self.id,
            "line_ids": [
                (
                    Command.create({
                        "name": "6% of selling price",
                        "quantity": 1,
                        "price_unit": (self.selling_price * 0.06)
                    })
                ),
                (
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00
                    })
                )
            ]
        }
        self.env["account.move"].sudo().create(invoice_vals)

        return super().action_sold()
