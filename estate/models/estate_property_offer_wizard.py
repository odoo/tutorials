from odoo import fields, models, api


class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'estate.property.offer.wizard model for the wizard'

    price = fields.Float(string='Offer Price', required=True)

    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)

    def action_create_offers(self):
        """

        properties that are not Sold or Cancelled  thn also creates an offer for each

        """

        self.ensure_one()

        new_offer = []
        eligible_property = self.env['estate.property'].search(
            [('state', 'not in', ['sold', 'cancelled', 'offer accepted'])]
        )

        for prop in eligible_property:
            new_offer.append(
                {
                    'price': self.price,
                    'partner_id': self.partner_id.id,
                    'property_id': prop.id,
                }
            )

        if new_offer:
            self.env['estate.property.offer'].create(new_offer)

        return {'type': 'ir.actions.act_window_close'}
