from odoo import Command, fields, models
from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        self.ensure_one()

        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        self.env['account.move'].create(
            {
                'name': f'INV/PROP/{fields.Date.today().year}/{self.id:05d}',
                'move_type': 'out_invoice',
                'partner_id': self.buyer_id.id,
                'invoice_line_ids': [
                    Command.create(
                        {
                            'name': self.name,
                            'quantity': 1,
                            'price_unit': self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            'name': '6% Fees',
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            'name': 'Adminstrative Fees',
                            'quantity': 1,
                            'price_unit': 100.0,
                        }
                    ),
                ],
            }
        )

        return super().action_set_sold()
