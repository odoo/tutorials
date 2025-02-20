from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged
from psycopg2.errors import CheckViolation


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstateTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties_new = cls.env["estate.property"].create(
            [
                {
                    "name": "test1",
                    "postcode": "1111",
                    "expected_price": 1000,
                    "living_area": 100,
                    "facades": 1,
                    "garage": False,
                    "garden": True,
                    "garden_area": 10,
                    "garden_orientation": "north",
                },
                {
                    "name": "test2",
                    "postcode": "1111",
                    "expected_price": 1000,
                    "living_area": 100,
                    "facades": 1,
                    "garage": False,
                    "garden": False,
                },
            ]
        )

        cls.properties_sold = cls.env["estate.property"].create(
            [
                {
                    "name": "test3",
                    "postcode": "1111",
                    "expected_price": 999,
                    "living_area": 100,
                    "facades": 1,
                    "garage": False,
                    "garden": False,
                    "state": "sold",
                    "selling_price": 1000,
                },
            ]
        )

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties_new.living_area = 20
        self.assertRecordValues(
            self.properties_new,
            [
                {"name": "test1", "total_area": 30},
                {"name": "test2", "total_area": 20},
            ],
        )

    def test_action_sell_property_at_zero_price(self):
        """Test that it is impossible to sell a property having price zero."""
        with self.assertRaises(CheckViolation):
            self.properties_new.action_set_sold()

    def test_action_create_offer_for_sold_property(self):
        """Test that it is impossible to create an offer for a sold property."""
        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create(
                [
                    {
                        "property_id": self.properties_sold[0].id,
                        "partner_id": 1,
                        "price": 1000,
                        "validity": 10,
                    },
                ]
            )
