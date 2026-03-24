from odoo.addons.estate.tests.common import EstateTestCommon
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstatePropertyTestCase(EstateTestCommon):
    def test_sell_property_with_no_offers(self):
        estate_property = self.create_property('offer_received')

        with self.assertRaises(UserError):
            estate_property.action_mark_as_sold()

    def test_sell_property_on_state_new(self):
        estate_property = self.create_property('new')

        with self.assertRaises(UserError):
            estate_property.action_mark_as_sold()

    def test_garden_reactivity(self):
        estate_property = self.create_property('new')

        with Form(estate_property) as form_estate_property:
            form_estate_property.garden = True
            form_estate_property.save()
            self.assertEqual(estate_property.garden_area, 10)
            self.assertEqual(estate_property.garden_orientation, 'north')

            form_estate_property.garden = False
            form_estate_property.save()
            self.assertEqual(estate_property.garden_area, 0)
            self.assertEqual(estate_property.garden_orientation, False)

            form_estate_property.garden = True
            form_estate_property.garden_area = 100
            form_estate_property.garden_orientation = 'south'
            form_estate_property.save()
            self.assertEqual(estate_property.garden_area, 100)
            self.assertEqual(estate_property.garden_orientation, 'south')
