from odoo import Command, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = "estate.property"

    def action_sold(self):
        
        for record in self:
            if not record.buyer_id:
                raise ValueError("The property must have a partner assigned before creating an invoice.")
            
            account_move = self.env['account.move'].sudo().create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Commission (6% of selling price)',
                        'quantity': 1,
                        'price_unit': record.selling_price*0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': '100.00',
                    }),
                ],
            })
            return super(EstateProperty, self).action_sold()
