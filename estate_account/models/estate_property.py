from odoo import fields, api, models, Command


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for estate in self:
            invoice_lines = [
                Command.create({
                    "name": f"Property {estate.name} (6% of estate's selling price)",
                    "quantity": 1,
                    "price_unit": estate.selling_price * 0.06
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100
                })
            ]
            account_move = {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": invoice_lines
            }
            estate.env["account.move"].create(account_move)

            return super().action_sold()
