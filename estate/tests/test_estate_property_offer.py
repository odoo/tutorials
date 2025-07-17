from odoo.exceptions import ValidationError, UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Buyer"})
        cls.property_type = cls.env["estate.property.types"].create({"name": "Apartment2"})
        cls.property = cls.env["estate.property"].create({
            "name": "Test Property",
            "expected_price": 150000,
            "property_type_id": cls.property_type.id
        })

    def test_cannot_create_offer_on_sold_property(self):
        self.property.state = "sold"
        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create({
                "price": 160000,
                "partner_id": self.partner.id,
                "property_id": self.property.id
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_set_state_sold()

    def test_cannot_sell_property_with_accepted_offer(self):
        offer = self.env["estate.property.offer"].create({
            "price": 160000,
            "partner_id": self.partner.id,
            "property_id": self.property.id
        })
        offer.action_accept_offer()
        self.property.action_set_state_sold()
        self.assertEqual(self.property.state, "sold")
        self.assertEqual(self.property.selling_price, offer.price)
        self.assertEqual(self.property.buyer_id, self.partner)

    def test_garden_fields_reset_on_uncheck(self):
        with Form(self.env["estate.property"]) as prop:
            prop.expected_price = 10000
            prop.name = "Test property"
            prop.garden = True
            prop.garden_area = 25
            prop.garden_orientation = "west"
        property = prop.save()

        with Form(property) as prop:
            prop.garden = False
        property = prop.save()

        self.assertEqual(property.garden_area, 0)
        self.assertFalse(property.garden_orientation)
