from odoo import models, Command


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["estate.property"]

    def action_sold(self):
        super().action_sold()
        journal = self.env["account.journal"].search([('type', '=', 'sale'), ('company_id', '=', self.env.company.id)])
        for record in self:
            self.env["account.move"].create({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "line_ids": [
                    Command.create({
                        "name": "Commission",
                        "quantity": 1.0,
                        "price_unit": 0.06 * record.selling_price,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.00,
                    })
                ]
            })
