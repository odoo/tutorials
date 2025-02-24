from odoo import  Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super().action_sold()

        self.check_access_rights('write')
        self.check_access_rule('write')

        if not self.buyer_id:
            raise ValueError("There is no buyer associated with the property")

        self.env['account.move'].sudo().create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'company_id': self.company_id.id,
            'invoice_line_ids': [
                # First Invoice line (60% of the selling price)
                Command.create({
                    'name': "Real Estate Commission Fee",
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
