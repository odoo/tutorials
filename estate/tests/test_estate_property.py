from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties = cls.env["estate.property"].create({
            "name": "Test Property 1",
            "expected_price": 1000,
        })

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(
            self.properties,
            [
                {"total_area": 20},
            ]
        )

    def test_action_set_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.properties.action_set_sold()
        self.assertRecordValues(
            self.properties,
            [
                {"state": "sold"},
            ]
        )

        # create an offer
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                "property_id": self.properties.id,
                "price": 2000,
                "partner_id": self.env.user.partner_id.id,
            })

        with self.assertRaises(UserError):
            self.properties.action_set_cancelled()
