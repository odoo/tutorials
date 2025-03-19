from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_status_sold(self):
        self.env['account.move'].create(
            {
                'partner_id': self.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': '6 Percent of selling price',
                        'quantity': 0.06,
                        'price_unit': self.selling_price
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1.0,
                        'price_unit': 100.0,
                    })
                ],
            }
        )
        return super().action_set_status_sold()
