from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold_state(self):
        super().action_set_sold_state()

        for record in self:
            move = self.env['account.move'].create(
                {'partner_id': record.buyer_id.id,
                 'move_type': 'out_invoice',
                 'line_ids': [
                     Command.create(
                         {
                             'name': record.name,
                             'quantity': 1,
                             'price_unit': record.selling_price * 0.06
                         }
                     ),
                     Command.create(
                         {
                             'name': 'Administrative Fee',
                             'quantity': 1,
                             'price_unit': 100
                         }
                     )
                 ]
                 })
        return move
