from odoo import models
from odoo.fields import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,  # .id because create() expects an ID, not a recordset
                "move_type": "out_invoice",  # 'out_invoice' is the technical name for 'Customer Invoice'
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "6% Commission of Selling Price",
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
                ],
            }
        )

        return super().action_property_sold()
