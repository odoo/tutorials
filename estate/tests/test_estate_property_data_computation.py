from odoo.tests import Form, TransactionCase, tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env["estate.property"].create([
            {
                "name": "Big Villa",
                "expected_price": 1000000,
                "living_area": 100,
                "garden": True,
                "garden_area": 50,
            },
            {
                "name": "Small Apartment",
                "expected_price": 200000,
                "living_area": 40,
                "garden": False,
            },
        ])

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.assertRecordValues(self.properties, [
            {"name": "Big Villa", "total_area": 150},
            {"name": "Small Apartment", "total_area": 40},
        ])
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
            {"name": "Big Villa", "total_area": 70},
            {"name": "Small Apartment", "total_area": 20},
        ])

    def test_garden_onchange(self):
        """Test that toggling garden updates garden area and garden_orientation."""
        with Form(self.properties[1]) as prop_form:
            prop_form.name = "Garden House"
            prop_form.expected_price = 500

            prop_form.garden = True
            self.assertEqual(prop_form.garden_area, 10)
            self.assertEqual(prop_form.garden_orientation, "north")
            prop_form.garden = False
            self.assertEqual(prop_form.garden_area, 0)
            self.assertFalse(prop_form.garden_orientation)

        self.assertRecordValues(self.properties[1], [{
            "garden": False,
            "garden_area": 0,
            "garden_orientation": False,
        }])
