from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        values = {
            "partner_id": self.salesperson_id.id,
            "move_type": "out_invoice",
            "journal_id": self.env["account.journal"].search([('type', '=', 'sale')], limit=1).id,
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price,
                }),
                Command.create({
                    "name": "6% commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                })
            ],
        }

        self.env["account.move"].create(values)
        return super().action_property_sold()
