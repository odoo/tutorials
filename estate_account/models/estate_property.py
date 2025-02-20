from odoo import Command, models


# using same name because we are inheriting the model from estate module
class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def action_sold(self):
        self.env["account.move"].sudo().create(
            {
                "move_type": "out_invoice",
                "partner_id": self.buyer_id.id,
                "line_ids": [
                    # First invoice line: Original Price of the Property
                    Command.create(
                        {
                            "name": f"{self.name} - Original Price",  # Description
                            "partner_id": self.buyer_id.id,
                            "price_unit": self.selling_price,  # Original selling price
                        }
                    ),
                    # Second invoice line: 6% of the Selling Price
                    Command.create(
                        {
                            "name": f"{self.name} - 6% of Selling Price",  # Description
                            "partner_id": self.buyer_id.id,
                            "price_unit": self.selling_price
                            * 0.06,  # 6% of selling price
                        }
                    ),
                    # Third invoice line: Administrative Fee of 100.00
                    Command.create(
                        {
                            "name": f"{self.name} - Administrative Fee",  # Description
                            "partner_id": self.buyer_id.id,
                            "price_unit": 100.00,  # Fixed administrative fee
                        }
                    ),
                ],
            }
        )
        return super(EstateProperty, self).action_sold()
