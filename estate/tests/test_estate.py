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
        super(EstateTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.prop1 = cls.env['estate.property'].create(
            {'name': 'prop1', 'living_area': 30, 'garden': False, 'expected_price': 1000, 'selling_price': 1000, 'status': 'sold'}
        )

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        # self.properties.living_area = 20
        self.assertRecordValues(self.prop1, [{'name': 'prop1', 'total_area': 30}])

    # def test_action_sell(self):
    #     """Test that everything behaves like it should when selling a property."""
    #     # self.prop1.action_sold()
    #     with self.assertRaises(UserError):
    #         self.prop1.action_sold()
    #     self.assertRecordValues(self.prop1, [{'status': 'new'}])

    def test_create_offer(self):
        with self.assertRaises(UserError):
            self.offer1 = self.env['estate.property.offer'].create(
            {'price': 990, 'property_id': self.prop1.id, 'partner_id': 10}
            )
