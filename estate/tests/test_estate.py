from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):

        super().setUpClass()

        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "Property1",
                    "expected_price": 1000000,
                    "living_area": 20,
                    "garden_area": 30,
                },
                {
                    "name": "Property2",
                    "expected_price": 2000000,
                    "living_area": 0,
                    "garden_area": 20,
                },
                {
                    "name": "Property3",
                    "expected_price": 3000000,
                    "living_area": 20,
                    "garden_area": 0,
                },
            ]
        )

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.assertRecordValues(
            self.properties,
            [
                {"name": "Property1", "total_area": 50},
                {"name": "Property2", "total_area": 20},
                {"name": "Property3", "total_area": 20},
            ],
        )

    def test_sold_then_create_offer(self):
        """Test that we cannot create a new offer after having sold a property."""
        property1 = self.properties[0]
        self.env["estate.property.offer"].create(
            [
                {
                    "price": 400000,
                    "partner_id": 1,
                    "property_id": property1.id,
                    "status": "accepted",
                }
            ]
        )
        property1.action_property_sold()
        self.assertEqual(property1.state, "sold")
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                [{"price": 400000, "partner_id": 1, "property_id": property1.id}]
            )

    def test_sell_no_accepted_offers(self):
        """Test that we cannot sell a property with no accepted offer."""
        for property in self.properties:
            with self.assertRaises(UserError):
                property.action_property_sold()

    def test_garden_checkbox(self):
        """Test the reset of the garden area and orientation when garden checkbox is ticked in the property form."""
        form = Form(self.env["estate.property"])
        form.name = "TestPropertyGarden"
        form.expected_price = 10
        # Untick garden
        form.garden = False
        record = form.save()
        self.assertEqual(record.garden, False)
        self.assertEqual(record.garden_area, 0)
        self.assertEqual(record.garden_orientation, False)
        # Tick garden
        form.garden = True
        record = form.save()
        self.assertEqual(record.garden, True)
        self.assertEqual(record.garden_area, 10)
        self.assertEqual(record.garden_orientation, "north")
        form.garden_area = 20
        form.garden_orientation = "south"
        record = form.save()
        # Untick garden
        form.garden = False
        record = form.save()
        self.assertEqual(record.garden, False)
        self.assertEqual(record.garden_area, 0)
        self.assertEqual(record.garden_orientation, False)
