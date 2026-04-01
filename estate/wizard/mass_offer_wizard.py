from odoo import fields, models


class MassOfferWizard(models.TransientModel):
    _name = 'mass.offer.wizard'
    _description = 'Mass Add Offers Wizard'

    type_id = fields.Many2one('estate.property.type', string="Property Type", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer Name", required=True)
    offer_price = fields.Integer(string="Offer Price", required=True)

    def action_add_offers(self):
        self.ensure_one()
        matching_properties = self.env['estate.property'].search([
            ('property_type_id', '=', self.type_id.id),
            ('expected_price', '<=', self.offer_price),
            ('state', 'not in', ['sold', 'canceled', 'offer_accepted']),
        ])

        offers = []
        for record in matching_properties:
            if record.best_price and record.best_price >= self.offer_price:
                continue
            offers.append({
                'property_id': record.id,
                'partner_id': self.customer_id.id,
                'price': self.offer_price,
            })

        self.env['estate.property.offer'].create(offers)
