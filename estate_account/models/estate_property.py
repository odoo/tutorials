# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import _, Command, api, fields, models

class Property(models.Model):
    _inherit = "estate.property"
    def action_sold(self):
        invoice_vals = {
            "name": "Invoice Bill",
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
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
        self.env["account.move"].create(invoice_vals)
        return super().action_sold()
