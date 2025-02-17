from odoo.tests import Form
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "Test Property 1",
                    "expected_price": 100,
                },
            ]
        )

        cls.offers = cls.env["property.offers"].create(
            [
                {
                    "partner_id": cls.env.ref("base.res_partner_12").id,
                    "property_id": cls.properties[0].id,
                    "price": 101,
                },
                {
                    "partner_id": cls.env.ref("base.res_partner_2").id,
                    "property_id": cls.properties[0].id,
                    "price": 100,
                },
            ]
        )

    def test_cannot_sell_property_without_accepted_offer(self):
        """Ensure that a property cannot be sold if there are no accepted offers."""
        with self.assertRaises(UserError):
            self.properties.action_sold()

    def test_selling_a_property_correctly_marks_it_as_sold(self):
        """Ensure that selling a property updates its state correctly."""

        # Accept an offer
        self.offers[0].action_accept()
        # Sell the property
        self.properties.action_sold()

        # Check that the property is now marked as sold
        self.assertEqual(self.properties.state, "sold")

    def test_cannot_create_offer_for_sold_property(self):
        """Ensure that once a property is sold, new offers cannot be created."""

        # Accept an offer and sell the property
        self.offers[0].action_accept()
        self.properties.action_sold()

        # Attempt to create a new offer for a sold property
        with self.assertRaises(UserError):
            self.env["property.offers"].create(
                {
                    "partner_id": self.env.ref("base.res_partner_2").id,
                    "property_id": self.properties[0].id,
                    "price": 102,
                }
            )

    def test_garden_uncheck_resets_values(self):
        """Ensure that unchecking the garden checkbox resets area and orientation."""
        property = self.properties[0]
        with Form(property) as form:
            form.garden = True
        self.assertEqual(property.garden_area, 10, "Garden Area should reset to 0")
        self.assertEqual(property.garden_orientation, "north")

        with Form(property) as form:
            form.garden = False
        self.assertEqual(property.garden_area, 0, "Garden Area should reset to 0")
        self.assertFalse(
            property.garden_orientation, "Garden Orientation should reset to False"
        )
