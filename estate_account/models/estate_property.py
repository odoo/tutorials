from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_property_as_sold(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'line_ids': [
                    Command.create(
                        {
                            'name': self.name,
                            'quantity': 1,
                            'price_unit': 0.06 * self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            'name': 'Administrative fees',
                            'quantity': 1,
                            'price_unit': 100,
                        }
                    ),
                ],
            }
        )
        return super().action_set_property_as_sold()
