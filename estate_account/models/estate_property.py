from odoo import models, Command


class EstatePropert(models.Model):
    _inherit = "estate.property"

    def action_set_property_sold(self):
        self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": "Comission",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administative Fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
        )
        return super().action_set_property_sold()
