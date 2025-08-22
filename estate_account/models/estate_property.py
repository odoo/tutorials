from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        result_super = super().action_property_sold()
        for single_property in self:
            self.env["account.move"].create(
                {
                    "partner_id": single_property.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "6%% of the selling price",
                                "quantity": 1,
                                "price_unit": 0.06 * single_property.selling_price,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1,
                                "price_unit": 100.0,
                            }
                        ),
                    ],
                }
            )
        return result_super
