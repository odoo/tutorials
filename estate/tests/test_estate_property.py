from odoo.tests import TransactionCase, Form
from odoo.exceptions import UserError

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it


# @tagged('estatetag')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        property_record_vals = {
            "state": "new",
            "name": "House in Mons/Hainaut",
            "expected_price": 150000.0,
        }
        cls.properties = cls.env['estate.property'].create(
            property_record_vals)

    def test_estate_property_sold_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.properties.action_sold()

    def test_estate_property_sold_has_state_sold(self):
        self.property_offers = self.env['estate.property.offer'].create([
            {"property_id": self.properties.id, "price": 145000},
        ])
        self.property_offers[0].action_accept()
        self.properties.action_sold()
        self.assertRecordValues(self.properties, [
            {'name': 'House in Mons/Hainaut', 'state': 'sold'},
        ])

    def test_estate_properties_garden_checkbox(self):
        with Form(self.properties) as form:
            form.garden = True
            self.assertEqual(form.garden_area, 10)
            self.assertEqual(form.garden_orientation, "north")
            form.garden = False
            self.assertEqual(form.garden_area, 0)
            self.assertFalse(form.garden_orientation)
