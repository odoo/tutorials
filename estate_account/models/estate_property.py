from odoo import Command, models


class Estate_account_model(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print("Overriding the action_sold method in the inherited model")
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.buyer_id.id,
            "invoice_line_ids": [
                Command.create({
                    "name": self.name + " - Commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,  # 6% of the selling price as commission
                }),
                Command.create({
                    "name": self.name + " - Admin fee",
                    "quantity": 1,
                    "price_unit": 100,
                }),
            ],
        })
        invoice.action_post()
        return super().action_sold()
