from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ADMINISTRATOR_ID = cls.env.ref("base.partner_admin").id
        cls.new_property = cls.env["estate.property"].create([{
            "name": "New Property",
            "state": "new",
            "expected_price": 1000.0
        }])
        cls.received_property = cls.env["estate.property"].create([{
            "name": "Received offer Property",
            "state": "received",
            "expected_price": 2000.0
        }])
        cls.accepted_property = cls.env["estate.property"].create([{
            "name": "Accepeted offer Property",
            "state": "accepted",
            "expected_price": 3000.0
        }])
        cls.sold_property = cls.env["estate.property"].create([{
            "name": "Sold Property",
            "state": "new",
            "expected_price": 4000.0
        }])
        cls.env["estate.property.offer"].create([{
            "partner_id": cls.ADMINISTRATOR_ID,
            "property_id": cls.sold_property.id,
            "status": "accepted",
            "price": 4000.0
        }])
        cls.sold_property.state = "sold"
        cls.cancelled_property = cls.env["estate.property"].create([{
            "name": "Cancelled Property",
            "state": "cancelled",
            "expected_price": 5000.0
        }])
        cls.env["estate.property.offer"].create([
            {
                "partner_id": cls.ADMINISTRATOR_ID,
                "property_id": cls.accepted_property.id,
                "status": "accepted",
                "price": 3000.0
            },
            {
                "partner_id": cls.ADMINISTRATOR_ID,
                "property_id": cls.received_property.id,
                "status": "refused",
                "price": 1999.0
            },
            {
                "partner_id": cls.ADMINISTRATOR_ID,
                "property_id": cls.received_property.id,
                "price": 2000.0
            }
        ])

    def test_offer_for_sold_property(self):
        offer_for_sold_property = {
            "partner_id": EstateTestCase.ADMINISTRATOR_ID,
            "property_id": self.sold_property.id
        }
        correct_offers = [
            {"partner_id": EstateTestCase.ADMINISTRATOR_ID, "property_id": self.new_property.id, "price": 1000},
            {"partner_id": EstateTestCase.ADMINISTRATOR_ID, "property_id": self.received_property.id, "price": 2000},
            {"partner_id": EstateTestCase.ADMINISTRATOR_ID, "property_id": self.accepted_property.id, "price": 3000},
            {"partner_id": EstateTestCase.ADMINISTRATOR_ID, "property_id": self.cancelled_property.id, "price": 5000},
        ]
        with self.assertRaises(UserError, msg="Creating an offer for a sold property should raise a UserError but it did not."):
            self.env["estate.property.offer"].create([offer_for_sold_property])
        for offer in correct_offers:
            self.env["estate.property.offer"].create([offer])

    def test_sell_property_with_no_accepted_offer(self):
        non_sellable_properties = [
            self.new_property,
            self.received_property
        ]
        for property in non_sellable_properties:
            with self.assertRaises(UserError):
                property.action_mark_as_sold()
        self.accepted_property.action_mark_as_sold()

    def test_sold_state_correctly_set(self):
        self.accepted_property.action_mark_as_sold()
        self.assertEqual(self.accepted_property.state, "sold", "When a property is sold, its state should be set to 'sold'.")

    def test_garden_area_orientation_reset(self):
        property_form = Form(self.env["estate.property"])
        self.assertFalse(property_form.garden)
        self.assertEqual(property_form.garden_area, 0)
        self.assertFalse(property_form.garden_orientation)
        property_form.garden = True
        self.assertTrue(property_form.garden)
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, "north")
        property_form.garden = False
        self.assertFalse(property_form.garden)
        self.assertEqual(property_form.garden_area, 0)
        self.assertFalse(property_form.garden_orientation)
