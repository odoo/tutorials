from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'House in Milan',
                'expected_price': 390000,
                'living_area': 120,
                'garden': True,
                'garden_area': 40
            },
            {
                'name': 'Castle in Dublin',
                'expected_price': 1200000,
                'living_area': 200,
                'garden': True,
                'garden_area': 80,
                'state': 'cancelled'
            },
        ])

        cls.partners = cls.env['res.partner'].create([
            {
                'name': 'Bill'
            },
            {
                'name': 'Bob'
            }
        ])

        cls.offers = cls.env['estate.property.offer'].create([
            {
                'price': 380000,
                'property_id': cls.properties[0].id,
                'partner_id': cls.partners[0].id
            },
            {
                'price': 396000,
                'property_id': cls.properties[0].id,
                'partner_id': cls.partners[1].id
            }
        ])

    def test_accept_offer(self):
        self.offers[0].accept_offer()
        self.assertEqual(self.offers[0].status, 'accepted')

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
           {'name': 'House in Milan', 'total_area': 60},
           {'name': 'Castle in Dublin', 'total_area': 100},
        ])

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""

        with self.assertRaises(UserError):
            self.properties.sell_property()
            self.assertRecordValues(self.properties, [
                {'name': 'House in Milan', 'state': 'sold'},
                {'name': 'Castle in Dublin', 'state': 'sold'},
            ])
