from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        # Ensures that the current user has write access to the property before creating an invoice.
        self.check_access_rights('write')
        self.check_access_rule('write')
        self.ensure_one()
        self.env["account.move"].sudo().create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": 0.06 * self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
        )
        return super().action_set_sold()