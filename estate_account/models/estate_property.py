from odoo import models, fields


class EstateProperty(models.Model):
    _inherit = ["estate.property"]
    _name = 'estate.property'

    moves = fields.Many2one("account.move", "Invoices")

    def action_sold(self):
        move = self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": 'out_invoice',
        })

        return super().action_sold()
