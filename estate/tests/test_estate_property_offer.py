from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Sold Property',
                'expected_price': 1_000,
                'state': 'sold'
            }, {
                'name': 'No Offer Property',
                'expected_price': 1_000,
            }, {
                'name': 'Property To Sell',
                'expected_price': 1_000
            }
        ])

        cls.offers = cls.env['estate.property.offer'].create([
            {
                'partner_id': 1,
                'property_id': cls.properties[2].id,
                'price': 1_000
            }
        ])

        cls.offers[0].accept_offer()

    def test_cannot_add_offer_to_sold_property(self):
        with self.assertRaises(UserError):
            self.properties[1].sell_property()

    def test_cannot_sell_property_with_no_offer(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([{
                'partner_id': 1,
                'property_id': self.properties[0].id,
                'price': 1000
            }])

    def test_property_marked_as_sold(self):
        self.assertEqual(self.properties[2].state, "offer-accepted")
        self.properties[2].sell_property()
        self.assertEqual(self.properties[2].state, "sold")
