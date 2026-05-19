from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class EstatePropertyTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.buyer = cls.env["res.partner"].create({"name": "Test Buyer"})
        cls.property_type = cls.env["estate.property.type"].create(
            {"name": "Test Type"}
        )
        cls.property = cls.env["estate.property"].create(
            {
                "name": "Test Property",
                "type_id": cls.property_type.id,
                "expected_price": 100000,
            }
        )

    def test_create_offer_for_sold_property(self):
        self.property.state = "sold"
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "property_id": self.property.id,
                    "partner_id": self.buyer.id,
                    "price": 90000,
                }
            )

    def test_sell_with_no_accepted_offers(self):
        self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "partner_id": self.buyer.id,
                "price": 90000,
            }
        )
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_sell_successful(self):
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "partner_id": self.buyer.id,
                "price": 90000,
            }
        )
        self.assertEqual(self.property.state, "offer_received")
        offer.action_set_accepted()
        self.assertEqual(self.property.state, "offer_accepted")
        self.property.action_set_sold()
        self.assertEqual(self.property.state, "sold")

    def test_garden_fields_reset_on_uncheck(self):
        with Form(self.property) as property_form:
            property_form.garden = True
            self.assertEqual(
                property_form.garden_area,
                10,
            )
            self.assertEqual(
                property_form.garden_orientation,
                "north",
            )
            property_form.garden = False
            self.assertEqual(
                property_form.garden_area,
                0,
            )
            self.assertFalse(property_form.garden_orientation)
