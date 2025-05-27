from odoo import Command, models


class EstateSoldInherited(models.Model):
    _inherit = 'estate.property'

    def action_property_sold(self):
        result = super().action_property_sold()
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create(
                        {
                            'name': f'The property {self.name}',
                            'quantity': 1,
                            'price_unit': self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            'name': f'Commission for property {self.name}',
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            'name': 'Administrative fees',
                            'quantity': 1,
                            'price_unit': 100.0,
                        }
                    ),
                ],
            }
        )
        return result
