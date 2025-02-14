# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models
from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        try:
            self.check_access("write")
        except AccessError:
            raise AccessError("You do not have permission to change the status of this property to sold")

        for property in self:
            invoice = self.env["account.move"].sudo().create({
                "name": "something something hello hunny bunny",
                "estate_property_id": property.id,
                "move_type": "out_invoice",
                "partner_id": property.buyer_id.id,
                "invoice_line_ids": [
                    Command.create(
                    {
                        "name": f"Commission of 6% for selling property {property.name}",
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
        return super().action_sold()
