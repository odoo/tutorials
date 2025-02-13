from odoo import models, fields, api, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):

        self.env['account.move'].create(
            {
            "name": "Invoice from Property %s" % (self.name),
            "move_type": 'out_invoice',
            "partner_id": self.buyer_id.id,
            "invoice_date": fields.Date.today(),
            "line_ids": [
                Command.create({
                    'name': 'Congrats on your new property',
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': 'Taxes',
                    'quantity': 1,
                    'price_unit': self.selling_price*0.06,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100,
                })
            ],
        }
        )
    
        return super().action_sold()
