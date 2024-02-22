from odoo import models, fields, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_to_sold(self):
        if self.state != 'accepted':
            raise UserError("The property must be in 'Offer Accepted' state to be sold.")
        if not self.partner_id:
            raise UserError("The property must have a customer assigned to create an invoice.")
        self._create_invoice()
        return super().action_set_to_sold()

    def _create_invoice(self):
        self.env['account.move'].create(
            {
                'partner_id': self.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Deposit (6%) : ' + self.name,
                        'price_unit': self.selling_price * 0.06,
                        'quantity': 1.0,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'price_unit': 100,
                        'quantity': 1.0,
                    }),
                ]
            }
        )
