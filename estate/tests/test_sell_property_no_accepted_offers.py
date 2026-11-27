from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class SellPropertyNoAcceptedOfferCase(TransactionCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()

        self.partner = self.env['res.partner'].create({
            'name': "Partner person"
        })
        self.property_no_offers = self.env['estate.property'].create({
            'name': "Property without offers",
            'expected_price': 100_000,
            'state': "new"
        })
        self.property_two_offers = self.env['estate.property'].create({
            'name': "Property with 2 offers",
            'expected_price': 100_000,
            'state': "new"
        })
        self.offer1 = self.env['estate.property.offer'].create({
            'price': 100_000,
            'state': "refused",
            'partner_id': self.partner.id,
            'property_id': self.property_two_offers.id
        })
        self.offer2 = self.env['estate.property.offer'].create({
            'price': 150_000,
            'state': "refused",
            'partner_id': self.partner.id,
            'property_id': self.property_two_offers.id
        })

    def test_sell_property_no_offer(self):
        with self.assertRaises(UserError):
            self.property_no_offers.action_sell_property()

    def test_sell_property_two_refused_offers(self):
        with self.assertRaises(UserError):
            self.property_two_offers.action_sell_property()
