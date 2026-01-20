from odoo.tests import Form, tagged
from odoo.exceptions import UserError
from odoo.addons.estate.tests.common import TestEstateCommon


@tagged('post_install', '-at_install')
class TestEstateProperty(TestEstateCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_action_sell_property(self):
        # Test failed case: Cancelled state
        with self.assertRaises(UserError):
            self.property_cancelled.action_sell_property()

        # Test failed case: No accepted offer
        with self.assertRaises(UserError):
            self.property_offer_received.action_sell_property()

        # Test successful case
        result = self.property_offer_accepted.action_sell_property()
        self.assertTrue(result)
        self.assertEqual(self.property_offer_accepted.state, 'sold')

    def test_onchange_garden(self):
        property_form = Form(self.env['estate.property'])

        # Test when garden is True
        property_form.garden = True
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, 'north')

        # Test when garden is False
        property_form.garden = False
        self.assertFalse(property_form.garden_area)
        self.assertFalse(property_form.garden_orientation)
