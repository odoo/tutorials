# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, Command, models
from odoo.exceptions import AccessError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        try:
            self.check_access("write")
        except AccessError:
            raise AccessError(_("You don't have permission to change/update the properties!"))

        result =  super().action_sold()

        for property in self:
            try:
                self.env["account.move"].sudo().create({
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
            except AccessError:
                raise AccessError(_("You do not have the required access rights to create an invoice. Please contact your administrator."))

        return result
