from odoo import  Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super().action_sold()

        if not self.buyer_id:
            raise ValueError("There is no buyer associated with the property")
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        if not journal:
            raise ValueError("There is no sales journal") 
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                # First Invoice line (60% of the selling price)
                Command.create({
                    'name': 'Real Estate Commission Fee',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.6 # commission fee which is 60% of selling price,
                }),
                # Second Invoice Line (fixed 100 fees)
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.0,  # fixed admin price
                })
            ]
        })
        return res
