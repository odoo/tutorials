from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.buyer = cls.env['res.partner'].create({'name': 'Test Buyer'})
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
        })

    def _create_offer(self, price=100000):
        return self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'buyer_id': self.buyer.id,
            'price': price,
        })

    def test_sell_property_without_accepted_offer(self):
        """A property cannot be sold if no offer has been accepted."""
        self._create_offer()
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_sell_property_with_accepted_offer(self):
        """Selling a property with an accepted offer marks it as sold."""
        self._create_offer().action_accept()
        self.property.action_sold()
        self.assertRecordValues(self.property, [{
            'state': 'sold',
            'selling_price': 100000,
            'buyer_id': self.buyer.id,
        }])

    def test_create_offer_on_sold_property(self):
        """No offer can be created once the property is sold."""
        self._create_offer().action_accept()
        self.property.action_sold()
        with self.assertRaises(UserError):
            self._create_offer(price=200000)

    def test_create_offer_on_property_with_accepted_offer(self):
        """No offer can be created once an offer has been accepted."""
        self._create_offer().action_accept()
        with self.assertRaises(UserError):
            self._create_offer(price=200000)
