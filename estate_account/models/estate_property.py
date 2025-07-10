from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        for record in self:
            partner_id = record.partner_id
            if partner_id:
                comission = record.selling_price * 0.06
                adminstration_fees = 100

                # creating an account move for invoicing
                self.env["account.move"].create(
                    {
                        "partner_id": partner_id.id,
                        "move_type": "out_invoice",
                        "line_ids": [
                            Command.create(
                                {
                                    "name": record.name,
                                    "quantity": 1,
                                    "price_unit": record.selling_price,
                                }
                            ),
                            Command.create(
                                {
                                    "name": "Commision",
                                    "quantity": 1,
                                    "price_unit": comission,
                                }
                            ),
                            Command.create(
                                {
                                    "name": "Admin Fees",
                                    "quantity": 1,
                                    "price_unit": adminstration_fees,
                                }
                            ),
                        ],
                    }
                )

        return super().action_sell_property()
