from odoo import models, Command


class InheritedEstateProperty(models.Model):
    _inherit="estate.property"
    
    def action_mark_property_sold(self):
        move = self.env["account.move"].create({
            "partner_id": self.buyer.id,
            "move_type": "out_invoice",
            "journal_id": self.env["account.journal"].search([("type", "=", "sale")], limit=1).id,
            "invoice_line_ids": [
                Command.create({
                    "name": "Property Sale Commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00
                }),
            ],
        })
        return super().action_mark_property_sold();
