from odoo import Command, models
from odoo.tools import float_utils as fu


class Property(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for property in self:
            self.env["account.move"].sudo().with_context(default_move_type="out_invoice").create({
                'partner_id': property.buyer_id.id,
                'journal_id': 1,
                'line_ids': [
                    Command.create({
                        "name": property.name,
                        "quantity": 1,
                        "price_unit": property.selling_price,
                    }),
                    Command.create({
                        "name": "6%% of selling price",
                        "quantity": 1,
                        "price_unit": fu.float_round((property.selling_price * 0.06), precision_rounding=0.01),
                    }),
                    Command.create({
                        "name": "administrative fees",
                        "quantity": 1,
                        "price_unit": 100_000,
                    })
                ]
            })
        return super().action_sold()
