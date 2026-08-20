from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

# === NO ===
# Create an offer for a sold property
# Sell a property with no accepted offers on it
# === NO ===

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstateTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.property_type = cls.env['estate.property.type'].create({'name': 'House'})
        cls.buyer = cls.env['res.partner'].create({'name': 'Test Buyer'})
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Property A',
                'postcode': '1000',
                'type_id': cls.property_type.id,
                'expected_price': 100000,
                'garden_area': 10,
            },
            {
                'name': 'Property B',
                'postcode': '2000',
                'type_id': cls.property_type.id,
                'expected_price': 200000,
                'garden_area': 30,
            },
        ])

    def test_sell_without_accepted_offer(self):
        """Selling a property with no accepted offers must fail."""
        with self.assertRaises(UserError):
            self.properties.action_sold()

    def test_offer_on_sold_property(self):
        """Creating an offer for a sold property must fail."""
        property = self.properties[0]
        offer = self.env['estate.property.offer'].create({
            'property_id': property.id,
            'partner_id': self.buyer.id,
            'price': property.expected_price,
        })
        offer.action_offer_accept()
        property.action_sold()

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': property.id,
                'partner_id': self.buyer.id,
                'price': property.expected_price * 2,
            })
