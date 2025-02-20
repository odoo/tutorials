from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        move = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(
            {
                'partner_id': self.partner_id.ids[0],
                'invoice_line_ids': [
                    Command.create(
                        {
                            'name': self.name,
                            'quantity': 1,
                            'price_unit': self.selling_price*0.06,
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

        return super().action_set_sold()
