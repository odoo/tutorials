from odoo.tests.common import TransactionCase
from odoo.tests import Form
from odoo.exceptions import UserError
from odoo.tests import tagged


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
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'house 1',
                'expected_price': 10,
            },
            {
                'name': 'house 2',
                'expected_price': 10,
            }
        ])

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
            {'name': 'house 1', 'total_area': 20},
            {'name': 'house 2', 'total_area': 20},
        ])

        self.properties[0].garden_area = 20

        with Form(self.properties[0]) as p:
            self.assertEqual(p.garden_area, 20)
            p.garden = True
            self.assertEqual(p.garden_area, 10)
            p.garden = False
            self.assertEqual(p.garden_area, 0)

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""

        # Can't sell properties without offers on them
        with self.assertRaises(UserError):
            self.properties.action_sell_listing()

        offers = self.env["estate.property.offer"].create([
            {
                'price': 7,
                'property_id': self.properties[0].id
            },
            {
                'price': 7,
                'property_id': self.properties[1].id
            }
        ])
        self.assertEqual(len(offers), 2)  # To silence unused var error

        self.properties.action_sell_listing()
        self.assertRecordValues(self.properties, [
            {'name': 'house 1', 'state': 'sold'},
            {'name': 'house 2', 'state': 'sold'},
        ])

        with self.assertRaises(UserError):
            self.properties[0].state = "cancelled"
            self.properties.action_sell_listing()

    def test_action_offer(self):
        """Test that everything behaves like it should when placing an offer."""

        offers = self.env["estate.property.offer"].create([{
            'price': 7,
            'property_id': self.properties[0].id
        }])

        # Acepting an offer with a price lower than 90% of expected price triggers an error
        with self.assertRaises(UserError):
            offers.action_accept_offer()

        # Placing an offer on a sold property should raise user error
        with self.assertRaises(UserError):
            self.properties[1].state = "sold"
            offers = self.env["estate.property.offer"].create([{
                'price': 10,
                'property_id': self.properties[1].id
            }])

        # Placing an offer lower than an existing offer triggers an error
        with self.assertRaises(UserError):
            offers = self.env["estate.property.offer"].create([{
                'price': 5,
                'property_id': self.properties[0].id
            }])
