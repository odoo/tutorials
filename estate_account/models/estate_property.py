# licence

from odoo import models
from odoo import Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        partner_id = self.salesperson_id.id
        move_type = 'out_invoice'
        # journal_id = self.env['account.journal'].search([])[0].id #  Tutorial chapter 13 incorrectly lists this field as being required
        self.env['account.move'].sudo().create({
            'partner_id': partner_id,
            'move_type': move_type,
            # 'journal_id': journal_id,
            'invoice_line_ids': [
                Command.create({'name': self.name, 'quantity': 0.06, 'price_unit': self.selling_price}),
                Command.create({'name': "Administrative fees", 'quantity': 1, 'price_unit': 100.00}),
            ],
            })
        return super().action_set_sold()
