from odoo import models, fields, Command


class Realestate(models.Model):
    _name = "realestate"
    _inherit = "realestate"

    def action_set_property_sold(self):
        self.env["account.move"].create(
            {
                "partner_id": super().buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": super().selling_price,
                        }
                    )
                ],
            }
        )
        return super().action_set_property_sold()
