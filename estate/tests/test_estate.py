from odoo.exceptions import UserError
from odoo.tests import Form, tagged, TransactionCase


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.buyer = cls.env["res.partner"].create({"name": "Test Buyer"})
        cls.property = cls.env["estate.property"].create(
            {
                "name": "Big Villa",
                "expected_price": 100000.0,
            }
        )
        cls.offer = cls.env["estate.property.offer"].create(
            {
                "partner_id": cls.buyer.id,
                "property_id": cls.property.id,
                "price": 95000.0,
            }
        )

    def test_create_offer_on_sold_property(self):
        self.offer.action_accept()
        self.property.action_sold()

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "partner_id": self.buyer.id,
                    "property_id": self.property.id,
                    "price": 110000.0,
                }
            )

    def test_create_offer_on_unsold_property_with_accepted_offer(self):
        self.offer.action_accept()
        self.assertEqual(self.property.state, "offer_accepted")

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "partner_id": self.buyer.id,
                    "property_id": self.property.id,
                    "price": 110000.0,
                }
            )

    def test_create_offer_on_unsold_property_without_accepted_offer(self):
        new_offer = self.env["estate.property.offer"].create(
            {
                "partner_id": self.buyer.id,
                "property_id": self.property.id,
                "price": 120000.0,
            }
        )
        self.assertEqual(self.offer.property_id, self.property)
        self.assertIn(new_offer, self.property.offer_ids)
        self.assertEqual(self.property.state, "offer_received")

    def test_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_sell_property_with_accepted_offer(self):
        self.offer.action_accept()
        self.property.action_sold()
        self.assertEqual(self.property.state, "sold")

    def test_garden_onchange_reset(self):
        with Form(self.env["estate.property"]) as prop_form:
            prop_form.name = "Garden House"
            prop_form.expected_price = 1000.0

            # Test garden checked
            prop_form.garden = True
            self.assertEqual(prop_form.garden_orientation, "north")
            self.assertEqual(prop_form.garden_area, 10)

            # Test garden customized
            prop_form.garden_area = 50
            prop_form.garden_orientation = "south"
            self.assertEqual(prop_form.garden_orientation, "south")
            self.assertEqual(prop_form.garden_area, 50)

            # Test garden unchecked
            prop_form.garden = False
            self.assertFalse(prop_form.garden_orientation)
            self.assertEqual(prop_form.garden_area, 0)
