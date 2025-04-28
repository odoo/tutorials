from odoo import models, Command


class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        res = super().action_sell_property()
        invoice_values = []
        for record in self:
            invoice_values.append({
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
            })
        for val in invoice_values:
            self.env["account.move"].create(val)
        return res
