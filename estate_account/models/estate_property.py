from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        sold = super().action_set_sold()
        for rec in self:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': rec.buyer_id.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': "%s Selling Price" % rec.name,
                        'quantity': 1,
                        'price_unit': rec.selling_price
                    }),
                    Command.create({
                        'name': 'Commission (6%)',
                        'quantity': 1,
                        'price_unit': rec.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100,
                    })
                ]
            })
        return sold
