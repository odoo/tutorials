from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_property_sold(self):
        for val in self:
            self.env['account.move'].create({
                'partner_id': val.buyer.id, 'move_type': 'out_invoice',
                'invoice_line_ids': [Command.create({'name': val.name, 'quantity': 1, 'price_unit': val.selling_price * 0.06}),
                                    Command.create({'name': 'administrative_fees', 'quantity': 1, 'price_unit': 100.00})]
                })
        return super().set_property_sold()
