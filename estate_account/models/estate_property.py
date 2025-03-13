from odoo import models, fields, api, Command
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        result = super().action_set_sold()

        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        if not journal:
            raise UserError("No sales journal found!")

        if not self.buyer:
            raise UserError("No buyer is assigned to this property!")

        invoice_vals = {
            "partner_id": self.buyer.id,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "invoice_line_ids": [
                Command.create({"name": "Property", "quantity": 1, "price_unit": self.selling_price}),
                Command.create({"name": "Service Fee (6%)", "quantity": 1, "price_unit": self.selling_price * 0.06}),
                Command.create({"name": "Administrative Fee", "quantity": 1, "price_unit": 100.00}),
            ],
        }

        invoice = self.env["account.move"].create(invoice_vals)
        
        return result
