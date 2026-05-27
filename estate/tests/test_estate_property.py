from .common import EstateTestCommon

from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class EstatePropertyTestCase(EstateTestCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property_offer_received = cls.env['estate.property'].create(
            {"name": "Test 3", "status": "offer_received", "expected_price": 100000})
        cls.property_offer_received.estate_property_offer_ids = cls.env['estate.property.offer'].create([
            {"estate_property_id": cls.property_offer_received.id, "buyer_id": 1, "price": 100000, "status": "new"},
            {"estate_property_id": cls.property_offer_received.id, "buyer_id": 1, "price": 100000, "status": "refused"},
        ])

        cls.property_cancelled = cls.env['estate.property'].create(
            {"name": "Test 4", "status": "cancelled", "active": True, "expected_price": 100000},
        )

        cls.property_offer_accepted = cls.env['estate.property'].create(
            {"name": "Test 5", "status": "offer_accepted", "expected_price": 100000})
        cls.property_offer_accepted.estate_property_offer_ids = cls.env['estate.property.offer'].create([
            {"estate_property_id": cls.property_offer_accepted.id, "buyer_id": 1, "price": 100000, "status": "accepted"},
            {"estate_property_id": cls.property_offer_accepted.id, "buyer_id": 1, "price": 100000, "status": "refused"},
        ])

    def test_compute_total_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
            {"name": "Test 0", "total_area": 20}, {"name": "Test 1", "total_area": 30}, {"name": "Test 2", "total_area": 70},
        ])

    def test_action_set_sold(self):
        """Test that a property is sold with the correct behavior.
            multiple properties: valueError
            canceled property: userError (cannot sell a canceled/inactive property)
            property with no accepted offer: userError (must accept at least 1 offer to sell)
            property with accepted offer: status set to sold
        """
        with self.assertRaises(ValueError):
            self.properties.action_set_sold()

        with self.assertRaises(UserError):
            self.property_cancelled.action_set_sold()

        with self.assertRaises(UserError):
            self.property_offer_received.action_set_sold()

        self.property_offer_accepted.action_set_sold()
        self.assertEqual(self.property_offer_accepted.status, "sold")

    def test_onchange_garden_orientation(self):
        """Test that the garden orientation is computed like it should."""
        property_form = Form(self.env['estate.property'])
        self.assertFalse(property_form.garden)
        self.assertEqual(property_form.garden_area, 0)
        self.assertFalse(property_form.garden_orientation)

        property_form.garden = True
        self.assertTrue(property_form.garden)
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, "north")

        property_form.garden = False
        self.assertFalse(property_form.garden)
        self.assertEqual(property_form.garden_area, 0)
        self.assertFalse(property_form.garden_orientation)
