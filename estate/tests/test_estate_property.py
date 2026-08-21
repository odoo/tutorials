from odoo.tests import Form, tagged

from odoo.addons.estate.tests.common import EstatePropertyCommon


@tagged("post_install", "-at_install")
class EstatePropertyGardenCase(EstatePropertyCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        main_property = cls.estate_properties.search([("name", "=", "Property 1")])
        main_property.living_area = 90
        main_property.garden = True
        main_property.garden_area = 100
        main_property.garden_orientation = "south"

    def test_garden_deactivation(self):
        """Test that when the Garden property is deactivated we get to see the change and deletion of previous values"""
        main_property = self.estate_properties.search([("name", "=", "Property 1")])
        with Form(main_property) as property:
            self.assertEqual(100, property.garden_area)
            self.assertEqual("south", property.garden_orientation)
            self.assertEqual(190, property.total_area)

            property.garden = False

            self.assertEqual(0, property.garden_area)
            self.assertEqual(False, property.garden_orientation)
            self.assertEqual(90, property.total_area)
