from odoo import Command, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    state = fields.Selection(selection_add=[('invoiced', 'Invoiced')], ondelete={'invoiced': 'cascade'})

    def action_create_invoice(self):
        super().action_create_invoice()
        self.env['account.move'].create({
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
