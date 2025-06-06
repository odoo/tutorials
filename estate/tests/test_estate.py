from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property = cls.env["estate.property"].create(
            {
                "name": "Sample Property",
                "description": "A test property for validation.",
                "living_area": 150,
                "garden": True,
                "garden_area": 50,
                "garden_orientation": "east",
                "state": "new",
                "expected_price": 100000,
            }
        )

        cls.property_1 = cls.env["estate.property"].create(
            {
                "name": "Sample Property 2",
                "description": "Another test property.",
                "living_area": 150,
                "garden": True,
                "garden_area": 50,
                "garden_orientation": "east",
                "state": "offer_accepted",
                "expected_price": 100000,
            }
        )

        cls.property_2 = cls.env["estate.property"].create(
            {
                "name": "Sample Property 3",
                "description": "A third test property.",
                "living_area": 150,
                "state": "new",
                "expected_price": 100000,
            }
        )

        cls.accepted_offer = cls.env["estate.property.offer"].create(
            {
                "property_id": cls.property.id,
                "partner_id": cls.env.ref("base.partner_demo").id,
                "price": 100000,
            }
        )
        cls.accepted_offer.action_accepted()

    def test_compute_total_area(self):
        """Verify that the total area calculation is correct."""
        self.property.living_area = 150
        self.assertRecordValues(
            self.property, [{"name": "Sample Property", "total_area": 200}]
        )

    def test_property_sale(self):
        """Ensure that a property can be sold correctly."""
        self.property.action_sold()
        self.assertRecordValues(
            self.property,
            [
                {"name": "Sample Property", "state": "sold"},
            ],
        )

    def test_sale_without_accepted_offer(self):
        """Ensure a property cannot be sold if no offer has been accepted."""
        with self.assertRaises(UserError):
            self.property_1.action_sold()

    def test_prevent_offers_on_sold_property(self):
        """Verify that offers cannot be made on properties already sold."""
        self.property_1.action_sold()
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "property_id": self.property_1.id,
                    "partner_id": self.env.ref("base.partner_demo").id,
                    "price": 150000,
                }
            )

    def test_correct_state_after_selling(self):
        """Check that the property state is updated correctly upon sale."""
        self.property.action_sold()
        self.assertRecordValues(
            self.property,
            [
                {"name": "Sample Property", "state": "sold"},
            ],
        )

    def test_garden_field_reset(self):
        """Ensure that garden area and orientation reset when garden is unchecked."""
        self.property_2.garden = True
        self.property_2.garden_area = 100
        self.property_2.garden_orientation = "north"

        self.property_2.garden = False
        self.property_2._onchange_garden()
        self.assertEqual(self.property_2.garden_area, 0)
        self.assertEqual(self.property_2.garden_orientation, False)
