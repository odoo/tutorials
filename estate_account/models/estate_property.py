from odoo import Command, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero


class EstatePropertyAccounting(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        if float_is_zero(self.selling_price, precision_rounding=0.01):
            raise UserError(
                "Atleast one offer must be accepted before selling the property"
            )
        values = {
            "partner_id": self.buyer.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": self.name,
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06,
                    }
                ),
                Command.create(
                    {
                        "name": "administrative_fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }
                ),
            ],
        }

        self.env["account.move"].create(values)

        return super().action_property_sold()
