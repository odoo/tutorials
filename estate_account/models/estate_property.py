from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_property(self):
        super().sold_property()
        for estateProperty in self:
            if not estateProperty.buyer_id:
                # Create invoice with no buyer doesn't make sense
                # Skip but could raise an error
                continue
            selling_price = estateProperty.best_price if estateProperty.best_price > 0.00 else estateProperty.expected_price
            accepted_offer = next(filter(lambda x: x.status == "Accepted", estateProperty.offer_ids), None)
            if accepted_offer and accepted_offer.price < selling_price:
                selling_price = accepted_offer.price
            self.env['account.move'].create({
                'partner_id': estateProperty.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': '6% of Selling price',
                        'quantity': 0.06,
                        'price_unit': selling_price
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.00
                    })
                ]
            })
        return True
