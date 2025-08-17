from odoo.tests.common import TransactionCase
from odoo.tests import Form , tagged
from odoo.exceptions import UserError

@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestEstateProperty, cls).setUpClass()

        # creating a property
        cls.property = cls.env['estate.property'].create({
            "name": "Test Property",
            "description": "This is a test property",
            "postcode": "22222",
            "expected_price": 1000,
            "bedrooms": 2,
            "living_area": 100,
            "facades": 2,
            "garage": True,
            "garden": True,
            "garden_area": 50,
            "garden_orientation": "north",
            "active": True,
            "state": "new",
        })

        # selecting buyer and property type from pre-made
        cls.property_buyer = cls.env["res.partner"].browse(1)
        cls.property_type = cls.env["estate.property.type"].browse('property_type_residential')

    def test_create_offer_for_sold_property(self):
        self.property.selling_price = 1000
        self.property.buyer_id = self.property_buyer
        self.property.action_set_property_status_sold()

        with self.assertRaises(UserError, msg="Sold Property cannot receive more offers"):
            self.env["estate.property.offer"].create({
                "property_id": self.property.id,
                "price": 1000.0,
                "partner_id": self.property_buyer.id
            })

    def test_sell_property_with_no_accepted_offer(self):
        # Remove all offers
        self.property.offer_ids.unlink()

        with self.assertRaises(UserError, msg="Property needs an accepted offer letter to be sold"):
            self.property.action_set_property_status_sold()

    def test_property_marked_sold(self):
        # This test assumes the property state has been set to sold in a previous operation.
        # Consider creating a fresh property if needed.
        self.assertEqual(self.property.state, "sold", "Property state should be sold")

    def test_garden_area_and_orientation_onchange(self):
        active_form = Form(self.property)
        initial_garden_area = active_form.garden_area
        initial_garden_orientation = active_form.garden_orientation

        # unchecking garden
        active_form.garden = False

        # testing that garden area and orientation do not reset
        self.assertEqual(active_form.garden_area, initial_garden_area, "Garden area should remain unchanged")
        self.assertEqual(active_form.garden_orientation, initial_garden_orientation, "Garden orientation should remain unchanged")

        # testing garden check is now false
        self.assertFalse(active_form.garden, "Garden should be false after unchecking")
