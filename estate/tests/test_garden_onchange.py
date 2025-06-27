from odoo.tests.common import TransactionCase

class TestGardenOnchange(TransactionCase):

    def test_garden_onchange_sets_defaults(self):
        """Ensure that enabling garden sets area and orientation"""
        prop = self.env["estate.property"].new({"garden": True})
        prop._onchange_garden()
        self.assertEqual(prop.garden_area, 10)
        self.assertEqual(prop.garden_orientation, "north")

    def test_garden_onchange_resets_fields(self):
        """Ensure that disabling garden resets area and orientation"""
        prop = self.env["estate.property"].new(
            {
                "garden": True,
                "garden_area": 15,
                "garden_orientation": "south",
            }
        )
        prop._onchange_garden()

        prop.garden = False
        prop._onchange_garden()

        self.assertEqual(prop.garden_area, 0)
        self.assertFalse(prop.garden_orientation)
