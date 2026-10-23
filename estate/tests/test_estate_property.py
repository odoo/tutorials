from odoo.exceptions import UserError
from odoo.tests import Form

from .common import EstateTestCommon


class TestEstateProperty(EstateTestCommon):
    def test_property_cant_be_sold_without_accepted_offer(self):
        with self.assertRaisesRegex(UserError, "accepted offer is required"):
            self.property_a.action_mark_sold()

    def test_state_is_sold_after_sold_action(self):
        self.property_a.offer_ids[0].action_accept()
        self.property_a.action_mark_sold()
        self.assertEqual(self.property_a.state, "sold")

    def test_garden_field_off_resets_area_and_orientation(self):
        with Form(self.property_a) as form:
            form.garden = True
            self.assertAlmostEqual(form.garden_area, 10)
            self.assertEqual(form.garden_orientation, "north")

            form.garden = False
            self.assertAlmostEqual(form.garden_area, 0)
            self.assertFalse(form.garden_orientation)
