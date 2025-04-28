from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        journal_id = self.env["account.journal"].search([("type", "=", "sale")],
                                                        limit=1)
        for val in self:
            self.env["account.move"].create({
                'partner_id': val.buyer_id.id,
                'move_type': "out_invoice",
                'journal_id': journal_id.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': val.name,
                        'quantity': 1.0,
                        'price_unit': val.selling_price * 6.0 / 100.0,
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1.0,
                        'price_unit': 100.0,
                    }),
                ],
            })
        return res
