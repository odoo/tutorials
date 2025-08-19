from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties = cls.env['estate.property'].create({'name': 'test'})

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
           {'name': 'test', 'total_area': '20'},
        ])

    def test_create_offer_for_solded_property(self):
        """Test that offers can't be create for solded properties."""
        self.properties.state = 'sold'
        with self.assertRaises(UserError, msg="Should not be able to create an offer for a sold property"):
            self.env['estate.property.offer'].create({
                    'property_id': self.properties.id,
                    'price': 150000.0,
        })

    def test_sell_property_with_no_offers(self):
        """Test that offers can't be create for solded properties."""
        with self.assertRaises(UserError, msg="Should not be able to sell a property with no offers"):
            self.properties.action_sold()
