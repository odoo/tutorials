"""Estate Property extension."""

from odoo import Command, models

class EstateProperty(models.Model):
    """Estate Property extension with inheritance to add invoice creation on sale."""
    
    _inherit = "estate.property"

    def action_set_sold(self):
        """Set the offer as sold."""
        move = self.env['account.move'].create(
            {
                'move_type': 'out_invoice',
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
