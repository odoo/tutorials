from odoo import api, models,Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        res = super().action_set_sold()  
        if not self.buyer_id:
            raise UserError("A buyer must be set before marking as sold.")
        
        self.env["account.move"].create({
            "partner_id": self.buyer_id.id, 
            "move_type": "out_invoice", 
            "journal_id": self.env["account.journal"].search([("type", "=", "sale")], limit=1).id,
            "invoice_line_ids": [
                Command.create({
                    "name": "Property Sale: " + self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06, 
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,  
                })
            ]
        })
        return res