from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        """Sell the properties, then invoice each buyer for the agency's commission."""
        if self.filtered(lambda estate_property: not estate_property.buyer_id):
            raise UserError(self.env._('A property needs a buyer before it can be sold.'))
        res = super().action_sold()
        self.env['account.move'].create([
            estate_property._prepare_invoice_values() for estate_property in self
        ])
        return res

    def _prepare_invoice_values(self):
        self.ensure_one()
        return {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': self.env._('6%% of the selling price of %s', self.name),
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': self.env._('Administrative fees'),
                    'quantity': 1,
                    'price_unit': 100.0,
                }),
            ],
        }
