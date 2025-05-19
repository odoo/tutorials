from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['estate_classic.property'].create({
            "name": "Cool House",
            "state": 'new',
            "expected_price": 100000,
        })
        cls.partner_a = cls.env['res.partner'].create({
                'name': 'partner_a',
            })

    def test_sell_property_without_offer_accepted_error(self):
        with self.assertRaises(ValidationError):
            self.property.state = 'sold'

    def test_selling_property(self):
        self.offer = self.env['estate_classic.property.offer'].create({
            "property_id": self.property.id,
            "partner_id": self.partner_a.id,
            "price": 105000,
        })
        self.offer.action_accept_offer()
        self.assertEqual(self.property.state, 'offer_accepted')
        self.property.action_sell_property()
        self.assertEqual(self.property.state, 'sold')
