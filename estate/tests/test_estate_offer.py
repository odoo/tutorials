from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged, Form


class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.properties = cls.env["estate.property"].create(
            {
                "name": "Test Property",
                "description": "test property",
                "postcode": "12345",
                "date_availability": "2024-12-31",
                "expected_price": 150000.0,
                "state": "new",
                "garden": True,
            }
        )
        cls.partner_id = cls.env["res.partner"].create({"name": "Farrahanitrate"})
        cls.offer1 = cls.env["estate.property.offer"].create(
            {
                "price": 140000.0,
                "property_id": cls.properties.id,
                "partner_id": cls.partner_id.id,
            }
        )
        cls.properties2 = cls.env["estate.property"].create(
            {
                "name": "Test Property2",
                "description": "test property2",
                "postcode": "12345",
                "date_availability": "2024-12-31",
                "expected_price": 150000.0,
                "state": "offer accepted",
            }
        )

    def test_offer_create_after_sold(self):
        self.properties2.action_sold()
        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create(
                {
                    "property_id": self.properties2.id,
                    "price": 210000.0,
                    "partner_id": self.partner_id.id,
                }
            )

    def test_no_sold_without_accept_offer(self):
        with self.assertRaises(UserError):
            self.properties.action_sold()

    def test_garden_toggle_check(self):
        with Form(self.properties) as form:
            form.garden = False
            self.assertEqual(
                form.garden_area,
                0,
                "Garden Area should be reset to 0 when Garden checkbox is unchecked",
            )
            self.assertEqual(
                form.garden_orientation,
                False,
                "Garden Orientation should be reset to False when Garden checkbox is unchecked",
            )
            form.garden = True
            form.garden = False
            self.assertEqual(
                form.garden_area,
                0,
                "Garden Area should be reset to 0 when Garden checkbox is unchecked",
            )
            self.assertEqual(
                form.garden_orientation,
                False,
                "Garden Orientation should be reset to False when Garden checkbox is unchecked",
            )
