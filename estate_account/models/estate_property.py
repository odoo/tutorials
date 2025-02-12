from odoo import models, Command
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"  

    def action_set_sold(self):
        """Overrides the Sold action to create an invoice before calling super()."""
        partner = self.buyer_id
        if not partner:
            raise UserError("Buyer must be set before selling the property.")

        invoice = self.env["account.move"].sudo().create({
            "partner_id": partner.id,
            "move_type": "out_invoice",
            # "journal_id": self.env["account.journal"].search([("type", "=", "sale")], limit=1).id,
            "invoice_line_ids": [
                Command.create({
                    "name": f"Property Name: {self.name}", 
                    "quantity": 1,
                    "price_unit": self.selling_price,
                }),
                Command.create({
                    "name": "Commission (6%)",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                }),
            ]
        })

        return super().action_set_sold()
