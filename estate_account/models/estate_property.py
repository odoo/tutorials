from odoo import Command, fields, models
from odoo.exceptions import AccessError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    state = fields.Selection(selection_add=[('invoiced', 'Invoiced')], ondelete={'invoiced': 'cascade'})

    def action_create_invoice(self):
        try:
            self.env['account.move'].check_access('write')
        except AccessError:
            raise AccessError("You don't have permission to update this property.")

        print(" reached ".center(100, '='))
        self.env['account.move'].sudo().create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price
                }),
                Command.create({
                    'name': 'Extra Charge (6%)',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100
                })
            ]
        })
        self.state = 'invoiced'
        return True
