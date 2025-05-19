from odoo import models, Command


class Realestate(models.Model):
    _name = "realestate_property"
    _inherit = "realestate_property"

    def action_set_property_sold(self):
        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": self.selling_price,
                        }
                    )
                ],
            }
        )
        return super().action_set_property_sold()
