from odoo import api, Command, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_status_sold(self):
        self.env["account.move"].sudo().create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    # Invoice for 6% of the selling price
                    Command.create(
                        {
                            "name": "Selling Commission (6%)",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    # Invoice for the administrative fees (fixed 100.00)
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
        return super().action_set_status_sold()
def action_set_status_draft(self):
    self.status = "new"
    return super().action_set_status_draft()
