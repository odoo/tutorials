from odoo import models, Command, _


class InheritedEstateProperties(models.Model):

    _inherit = "estate.property"

    def sold_property_button_action(self):
        super().sold_property_button_action()

        for property in self:
            invoice_data = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': _("Agent commission for house: %s", property.name),
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
        return
