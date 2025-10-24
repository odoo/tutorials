from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create({"name": "Test house", "expected_price": 240000})
        cls.partner = cls.env['res.partner'].create({"name": "Partner"})

    def test_offer_creation(self):
        """Test that the offer cannot be created if the property is sold."""
        self.env['estate.property.offer'].create({"price": 240000, "partner_id": self.partner.id, "property_id": self.properties.id, 'status': 'accepted'})
        self.properties.state = 'sold'

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({"price": 240000, "partner_id": self.partner.id, "property_id": self.properties.id})

    def test_property_selling(self):
        """Test that the property cannot be sold if no accepted offer."""
        with self.assertRaises(UserError):
            self.properties.state = 'sold'

        self.env['estate.property.offer'].create({"price": 240000, "partner_id": self.partner.id, "property_id": self.properties.id, 'status': 'accepted'})
        self.properties.state = 'sold'

    def test_garden_fields_reset(self):
        estate_property_form = Form(self.env['estate.property'].with_context({"name": "Test garden", "expected_price": 320000}))

        estate_property_form.garden = True
        estate_property_form.garden_orientation = 'east'
        estate_property_form.garden_area = 120

        self.assertEqual(estate_property_form.garden_orientation, "east")
        self.assertEqual(estate_property_form.garden_area, 120)

        estate_property_form.garden = False
        self.assertEqual(estate_property_form.garden_orientation, "north")
        self.assertEqual(estate_property_form.garden_area, 10)

        estate_property_form.garden = True
        self.assertEqual(estate_property_form.garden_orientation, "north")
        self.assertEqual(estate_property_form.garden_area, 10)
