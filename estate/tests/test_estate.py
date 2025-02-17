from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    def setUp(self):
        super(EstateTestCase, self).setUp()
        self.property_type = self.env["estate.property.type"].create({"name": "Mansion"})
        self.buyer = self.env["res.partner"].create({"name": "Alex Smith"})
        self.property = self.env["estate.property"].create({
            "name": "Grand Mansion",
            "expected_price": 750000.0,
            "property_type_id": self.property_type.id
        })
        self.offer = self.env["estate.property.offer"].create({
            "property_id": self.property.id,
            "price": 760000.0,
            "status": "accepted",
            "partner_id": self.buyer.id
        })

    def test_cannot_create_offer_for_sold_property(self):
        self.property.selling_price = 760000.0
        self.property.buyer_id = self.buyer
        self.property.action_sold()

        with self.assertRaises(UserError, msg="A sold property cannot receive offers!"):
            self.env["estate.property.offer"].create({
                "property_id": self.property.id,
                "price": 770000.0,
                "partner_id": self.buyer.id
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        self.property.offer_ids.unlink()
        with self.assertRaises(UserError, msg="You cannot sell a property without an accepted offer."):
            self.property.action_sold()

    def test_property_marked_as_sold_correctly(self):
        self.property.selling_price = 760000.0
        self.property.buyer_id = self.buyer
        self.property.action_sold()
        self.assertEqual(self.property.status, "sold", "Property should be marked as sold.")
