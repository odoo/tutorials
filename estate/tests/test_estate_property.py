from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged

@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.property = cls.env["estate.property"].create({
            "name": "Property 1",
            "living_area": 20,
            "expected_price": 10394,
            "garden": True,
        })
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})

    def test_offer_creation_and_selling_without_accepted_offer_should_fail(self):
        
        # Attempt to sell a property without an accepted offer
        with self.assertRaises(UserError):
            self.property.action_set_sold()

        # Attempt to create an offer for a sold property
        offer = self.env["estate.property.offer"].create({
            "property_id": self.property.id,
            "price": 40000,
            "partner_id": self.partner.id,
        })
        offer.action_accept_offer()
        self.property.action_set_sold()

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create({
                "property_id": self.property.id,
                "price": 40000,
                "partner_id": self.partner.id,
            })

        # Checking propety is correctly marked as sold
        self.assertEqual(
            self.property.state, "sold", "The property should be marked as sold."
        )

    def test_reset_garden_area_and_orientation_when_garden_is_unchecked(self):
        estate_form = Form(self.property)
        estate_form.garden = False
        self.assertEqual(estate_form.garden_orientation, False)
        self.assertEqual(estate_form.garden_area, 0)

        estate_form.garden = True
        self.assertEqual(estate_form.garden_orientation, "north")
        self.assertEqual(estate_form.garden_area, 10)
