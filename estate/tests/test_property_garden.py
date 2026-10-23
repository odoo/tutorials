from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestPropertyGarden(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env["estate.property"].create(
            {
                "name": "Garden House",
                "expected_price": 250000,
            }
        )

    def test_garden_onchange_reset(self):
        property_form = Form(self.property)

        property_form.garden = True
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, "north")

        property_form.garden = False

        self.assertFalse(property_form.garden_area)
        self.assertFalse(property_form.garden_orientation)
