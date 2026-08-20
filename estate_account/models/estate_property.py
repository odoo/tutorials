
from odoo import Command, models
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        """Create the invoice for the sold property and then mark it as sold with the original method. The invoice created will include 2 items:
        the 6% of the selling price and a fixed administrative fee of 100.0.

        Raises:
            ValidationError: If the property is not in the "offer_accepted" state, if there are no offers for the property, or if there is no accepted offer.
        """
        self.ensure_one()

        if not self.offer_ids:
            raise ValidationError("No offers found for this property.")

        accepted_offer = self.offer_ids.filtered(lambda o: o.status == "accepted")
        if not accepted_offer:
            raise ValidationError("No accepted offer found for this property.")

        self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_line_ids': [
                Command.create({
                    'name': f"Property: {self.name} - Offer by {self.partner_id.name}",
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': "Administrative Fees",
                    'quantity': 1,
                    'price_unit': 100.0,
                }),
            ],
        })

        return super(EstateProperty, self).action_sold()
