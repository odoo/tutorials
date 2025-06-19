from odoo import Command, _, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_to_sold(self):
        result = super().set_to_sold()
        for property in self:
            invoice_data = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': _("Down Payment For %s", property.name),
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06
                    }),
                    Command.create({
                        'name': _("Administration Fees"),
                        'quantity': 1,
                        'price_unit': 100.00
                    })
                ]
            }
            self.env['account.move'].create(invoice_data)
        return result
