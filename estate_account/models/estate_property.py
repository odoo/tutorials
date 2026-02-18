from odoo import models
from odoo.orm.commands import Command


class EstateProperty(models.Model):

    # -------------------------------------------------------------------------
    # Private attributes
    # -------------------------------------------------------------------------
    _inherit = "estate.property"

    # -------------------------------------------------------------------------
    # Action methods
    # -------------------------------------------------------------------------
    def action_sold_property(self):
        self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 0.06,
                    "price_unit": self.selling_price,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                })
            ],
        })
        return super().action_sold_property()
