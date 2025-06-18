from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_to_sold(self):
        for record in self:
            invoice_data = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': f"Down Payment For {record.name}",
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06
                    }),
                    Command.create({
                        'name': "Administration Fees",
                        'quantity': 1,
                        'price_unit': 100.00
                    })
                ]
            }
            self.env['account.move'].create(invoice_data)
        return super().set_to_sold()
