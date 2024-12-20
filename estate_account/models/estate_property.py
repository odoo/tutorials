from odoo import models, Command


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            record.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "Selling Fee",
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06
                    }),        
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100,
                    }),
            ]})
        return super(EstateProperty, self).action_sold()

