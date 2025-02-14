from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'
    
    def sold_property(self):
        invoice_record = self.env['account.move'].create({
            'partner_id':self.buyer_id.id,
            'move_type':'out_invoice',
            'journal_id': self.env['account.journal'].search(domain=[('name','=','Customer Invoices')],limit=1).id,
            'currency_id':20,
            'invoice_line_ids': [
                    Command.create({
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price,
                    }),
                    Command.create({
                        'name': "Selling price commission (6%)",
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            }),
        return super().sold_property()