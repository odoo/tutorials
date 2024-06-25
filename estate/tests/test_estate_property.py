from odoo.exceptions import ValidationError
from odoo.tests import Form

from .test_estate_common import EstateCommonTest


class TestProperty(EstateCommonTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env["estate.property"].create(
            {"expected_price": 100, "a_new_field_two": "Hello", "state": "new"}
        )

    def test_sell_property_without_accepted_offer(self):
        with self.assertRaises(ValidationError):
            self.property.action_sold()

        self.env["estate.property.offer"].create(
            {
                "price": 100,
                "property_id": self.property.id,
                "partner_id": self.partner.id,
                "status": "refused",
            }
        )
        with self.assertRaises(ValidationError):
            self.property.action_sold()

    def test_sell_property_with_accepted_offer(self):
        self.env["estate.property.offer"].create(
            {
                "price": 100,
                "property_id": self.property.id,
                "partner_id": self.partner.id,
                "status": "accepted",
            }
        )

        self.property.action_sold()
        self.assertEqual(self.property.state, "sold")

    def test_garden_options_on_change(self):
        estate_property = Form(self.env["estate.property"])
        estate_property.garden = True
        self.assertEqual(estate_property.garden_area, 10)
        self.assertEqual(estate_property.garden_orientation, "north")

        estate_property.garden = False
        self.assertEqual(estate_property.garden_area, 0)
        self.assertEqual(estate_property.garden_orientation, False)
