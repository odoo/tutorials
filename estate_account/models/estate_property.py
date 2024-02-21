from odoo import fields, models, Command

from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for property_sold in self:
            invoice_vals = {
                'name': f'INV/PROP/{property_sold.id}',
                'move_type': 'out_invoice',
                'partner_id': property_sold.buyer_id.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': property_sold.name,
                        'price_unit': property_sold.selling_price,
                        'quantity': 1
                    }),
                    Command.create({
                        'name': '6% additional cost',
                        'price_unit': property_sold.selling_price * .06,
                        'quantity': 1
                    }),
                    Command.create({
                        'name': 'Administration fees',
                        'price_unit': 100,
                        'quantity': 1
                    })
                ]
            }

            self.env['account.move'].create(invoice_vals)

        return super().action_set_sold()
