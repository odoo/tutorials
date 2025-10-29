from odoo import models, fields, Command
from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):

        try:
            self.check_access("write")
        except AccessError:
            raise AccessError("You are not allowed to sell this property. Contact your manager.")

        self.env["account.move"].sudo().create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_date": fields.Date.context_today(self),
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
                            "name": "Administration fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
        )

        return super().action_set_sold()
