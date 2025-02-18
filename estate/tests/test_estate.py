from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged

@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        # Create dummy data for testing
        cls.property = cls.env['estate.property'].create({
            "name": "Test Property",
            "living_area": 20,
            "expected_price": 10394,
            "garden": True,
        })
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})

    def test_offer_creation_on_sold_property(self):
        print(" Test 1 : Sold Property test case execute ".center(100,"-"))
        self.property.status = "sold"
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create({
                "price": 135000,
                "property_id": self.property.id,
                "partner_id": self.partner.id
            })

    def test_property_without_accepted_offer_should_fail(self):
        print(" Test 2 : Property cannot be sold without accepting the offer ".center(100,"-"))
        with self.assertRaises(UserError):
            self.property.action_property_sold()

    def test_reset_garden_area_and_garden_orientation_when_garden_is_unchecked(self):
        print(" Test 3 : Garden button with their linked properties behaviour  checkup".center(100, "-"))
        estate_form = Form(self.property)

        estate_form.garden = False
        self.assertEqual(estate_form.garden_orientation, False)
        self.assertEqual(estate_form.garden_area, 0)
        
        estate_form.garden = True
        self.assertEqual(estate_form.garden_orientation, "north")
        self.assertEqual(estate_form.garden_area, 10)


