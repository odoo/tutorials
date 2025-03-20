from odoo import api, Command, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'
    
    def mark_sold(self):
        for record in self:
            line_defs = [
                {
                    'name': f'selling price (6% of {record.selling_price})',
                    'quantity': 1,
                    'price_unit': 0.06*record.selling_price
                },
                {
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 100
                },
            ]
            lines = [Command.create(line) for line in line_defs]
            values = {'partner_id': record.buyer.id, 'move_type': 'out_invoice', 'line_ids': lines}
            moves = self.env['account.move'].create(values)
        return super().mark_sold() 
