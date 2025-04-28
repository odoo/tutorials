from odoo import models, Command


class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        for record in self:
            invoice_dictionary = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": self.env['account.journal'].search([("code", "=", "INV")]).id,
                "line_ids": [
                    Command.create({
                        "name": "Selling Price Percentage",
                        "quantity": "1",
                        "price_unit": record.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": "1",
                        "price_unit": "100",
                    })
                ]
            }
            self.env["account.move"].create(invoice_dictionary)
            super().action_sell_property()
