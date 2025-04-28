from odoo import models, Command


class EstateAccountProperty(models.Model):
    # ------------------
    # Private attributes
    # ------------------

    _inherit = "estate.property"
    _description = "This class allows to link Accounting App with Estate App."

    # --------------
    # Action methods
    # --------------

    def action_sell_offer(self):
        self.ensure_one()
        for record in self:
            account_move = {
                "move_type": "out_invoice",
                "journal_id": self.env["account.journal"].search([('type', '=', 'sale')]).id,
                "partner_id": record.buyer_id.id,
                "line_ids": [
                   Command.create({
                       "name": "6% of the property price",
                       "quantity": "1",
                       "price_unit": record.selling_price * 0.06
                   }),
                   Command.create({
                       "name": "Administrative fees",
                       "quantity": "1",
                       "price_unit": 100.00
                   })
                ]
            }
        self.env["account.move"].create(account_move)
        return super().action_sell_offer()
