from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):
        super().sold_property()
        invoices_to_create = []

        for estate_property in self.filtered('buyer_id'):
            selling_price = estate_property.best_price or estate_property.expected_price

            accepted_offers = estate_property.offer_ids.filtered(lambda x: x.status == 'accepted')

            if accepted_offers:
                min_accepted_offer = min(accepted_offers.mapped('price'))
                selling_price = min(selling_price, min_accepted_offer)

            invoice_data = {
                'partner_id': estate_property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "6% of Selling price",
                        'quantity': 0.06,
                        'price_unit': selling_price,
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100.00,
                    })
                ]
            }
            invoices_to_create.append(invoice_data)

            if invoices_to_create:
                self.env['account.move'].create(invoices_to_create)

        return True
