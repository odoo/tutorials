from .common import EstateTestCommon

from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstatePropertyOfferTestCase(EstateTestCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property_offer_received = cls.env['estate.property'].create(
            {"name": "Test 3", "status": "offer_received", "expected_price": 100000})
        cls.property_offer_received.estate_property_offer_ids = cls.env['estate.property.offer'].create([
            {"estate_property_id": cls.property_offer_received.id, "buyer_id": 1, "price": 100000, "status": "new"},
            {"estate_property_id": cls.property_offer_received.id, "buyer_id": 1, "price": 100000, "status": "refused"},
        ])

        cls.property_sold = cls.env['estate.property'].create(
            {"name": "Test 4", "status": "sold", "expected_price": 100000})

        cls.property = cls.env['estate.property'].create(
            {"name": "Test 5", "expected_price": 100000})

    def test_create(self):
        """Test that an offer is created with the correct behavior
            price lower than current lowest: userError (must be >= current lowest offer)
            property already sold: userError (cannot offer on sold property)
            no other offer exists: success case
            successful offer: create offer, and set property status to "offer_received" IFF status == "new"
        """
        with self.assertRaises(UserError):  # lower than current lowest
            self.env["estate.property.offer"].create({
                "estate_property_id": self.property_offer_received.id,
                "buyer_id": 1,
                "price": 100})

        with self.assertRaises(UserError):  # already sold
            self.env["estate.property.offer"].create({
                "estate_property_id": self.property_sold.id,
                "buyer_id": 1,
                "price": 100000})

        self.assertEqual(self.property.status, "new")
        self.env["estate.property.offer"].create({  # no other offer exists
            "estate_property_id": self.property.id,
            "buyer_id": 1,
            "price": 100000})
        self.assertEqual(self.property.status, "offer_received")
        self.assertEqual(len(self.property.estate_property_offer_ids), 1)

        self.env["estate.property.offer"].create({  # existing offer exists
            "estate_property_id": self.property.id,
            "buyer_id": 1,
            "price": 100000})
        self.assertEqual(self.property.status, "offer_received")
        self.assertEqual(len(self.property.estate_property_offer_ids), 2)
