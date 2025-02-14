# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        result =  super().action_sold()
        for property in self:
            self.env["account.move"].create({
                "move_type": "out_invoice",
                "partner_id": property.buyer_id.id,
                "invoice_line_ids": [
                    Command.create(
                    {
                        "name": property.name,
                        "quantity": 1,
                        "price_unit": property.selling_price * 6.0 / 100.0,
                    }
                    ),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ]
            })
        return result
