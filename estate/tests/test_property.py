from odoo.tests import TransactionCase, Form
from odoo.exceptions import UserError


class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.test_property = cls.env["estate.property"].create({
            "name": "Test",
            "state": "new",
            "expected_price": 50000.00,
            "garden": True,
            "garden_area": 30,
            "garden_orientation": "south",
        })
        cls.test_valid_offer = cls.env["estate.property.offer"].create([
            {
                "partner_id": cls.test_partner.id,
                "property_id": cls.test_property.id,
                "price": 50000.00,
            }
        ])

    def test_create_property_offer_on_sold_property(self):
        self.test_valid_offer.action_accept()
        self.test_property.action_set_property_sold()
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create([
                {
                    "partner_id": self.test_partner.id,
                    "property_id": self.test_property.id,
                    "price": 51000.00,
                }
            ])

    def test_sell_property_with_no_accepted_offers(self):
        with self.assertRaises(UserError):
            self.test_property.action_set_property_sold()

    def test_property_state_after_selling(self):
        self.test_valid_offer.action_accept()
        self.test_property.action_set_property_sold()
        self.assertEqual(self.test_property.state, "sold")

    def test_garden_fields_reset_form(self):
        with Form(self.test_property) as f:
            f.garden = False
            self.assertEqual(f.garden_area, 0)
            self.assertFalse(f.garden_orientation)

            f.garden = True
            self.assertEqual(f.garden_area, 10)
            self.assertEqual(f.garden_orientation, "north")
