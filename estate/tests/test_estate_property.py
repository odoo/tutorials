from odoo.exceptions import UserError
from odoo.tests import Form, TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.buyer = cls.env['res.partner'].create({'name': 'Test Buyer'})
        cls.estate_property = cls.env['estate.property'].create({
            'name': 'Test Villa',
            'expected_price': 100000,
        })

    def _create_offer(self, price):
        return self.env['estate.property.offer'].create({
            'property_id': self.estate_property.id,
            'partner_id': self.buyer.id,
            'price': price,
        })

    def test_sell_property_with_accepted_offer(self):
        """A property with an accepted offer can be sold and is marked as sold."""
        self._create_offer(95000).action_accept()

        self.estate_property.action_sold()

        self.assertRecordValues(self.estate_property, [{
            'state': 'sold',
            'selling_price': 95000,
            'buyer_id': self.buyer.id,
        }])

    def test_sell_property_without_accepted_offer(self):
        """A property cannot be sold without an accepted offer, even if it has offers."""
        # Set a buyer so that only the accepted-offer rule can block the sale
        # (estate_account, when installed, also requires a buyer).
        self.estate_property.buyer_id = self.buyer

        with self.assertRaises(UserError):
            self.estate_property.action_sold()

        self._create_offer(95000)
        with self.assertRaises(UserError):
            self.estate_property.action_sold()

        self.assertNotEqual(self.estate_property.state, 'sold')

    def test_sell_property_twice(self):
        """An already sold property cannot be sold again."""
        self._create_offer(95000).action_accept()
        self.estate_property.action_sold()

        with self.assertRaises(UserError):
            self.estate_property.action_sold()

    def test_create_offer_on_sold_property(self):
        """No offer can be created on a sold property."""
        self._create_offer(95000).action_accept()
        self.estate_property.action_sold()

        with self.assertRaises(UserError):
            self._create_offer(99000)

    def test_create_offer_on_cancelled_property(self):
        """No offer can be created on a cancelled property."""
        self.estate_property.action_cancel()

        with self.assertRaises(UserError):
            self._create_offer(95000)

    def test_garden_onchange(self):
        """Unchecking the garden resets its area and orientation."""
        with Form(self.env['estate.property']) as property_form:
            property_form.name = 'Garden House'
            property_form.expected_price = 100000

            property_form.garden = True
            self.assertEqual(property_form.garden_area, 10)
            self.assertEqual(property_form.garden_orientation, 'north')

            property_form.garden = False
            self.assertEqual(property_form.garden_area, 0)
            self.assertFalse(property_form.garden_orientation)
