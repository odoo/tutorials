from odoo import models, Command
from odoo.exceptions import AccessError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    # -------- Overridden Method -----------
    def action_property_sold(self):
        print(" The overriden mehtod from estate module is being called".center(150, '='))  

        # //TODO : Explore this while referring restricted data chapter
        if not self.env['account.move'].check_access('create'):
            try:
                self.check_access('write')
            except AccessError:
                raise AccessError("You do not have permission to sell this property.")
            
        self.env['account.move'].sudo().create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": 0.6 * self.selling_price
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.00
                        }
                    )
                ]
            }
        )

        return super().action_property_sold()
