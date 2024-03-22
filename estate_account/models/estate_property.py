"""module for child model linking invoicing to estate.property"""

from odoo import Command, models

class EstatePropertyChild(models.Model):
    "Child model linking invoicing to estate.property"
    _inherit="estate.property"

    def action_set_sold(self):
        success = super().action_set_sold()
        if success and self.buyer_id and self.selling_price:
            invoice_line_data = [
                {"name": f"{self.name} pro rata (6%)", "quantity": 1, "price_unit": self.selling_price * 0.06 },
                {"name": "Admin Fees", "quantity": 1, "price_unit": 100.},
                ]
            self.env["account.move"].create({
                "move_type": "out_invoice",
                "partner_id": self.buyer_id.id,
                "line_ids": [Command.create(line) for line in invoice_line_data],
                })
        return success
