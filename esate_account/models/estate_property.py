from odoo import Command, models, api
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):

    _inherit = "estate.property"

    def action_set_sold(self):
        if not self.buyer_id:
            raise ValidationError("No buyer assigned! Cannot create an invoice.")
        invoice = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name':'6% of the selling price',
                    'quantity':'1',
                    'price_unit':self.selling_price*0.06
                }),
                Command.create({
                    'name':'administrative fees',
                    'quantity':'1',
                    'price_unit':100
                })
            ]
        }
        self.env['account.move'].create(invoice)
        return super().action_set_sold()
