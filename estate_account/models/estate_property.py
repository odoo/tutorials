from odoo import models
from odoo.fields import Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for property in self:
            property.check_access_rights("write")
            property.check_access_rule("write")

            self.env["account.move"].sudo().create({
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": "6% Commission",
                        "quantity": 1,
                        "price_unit": property.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }),
                ],
            })

        return super().action_sold()
