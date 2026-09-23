from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Initialize buyer and property data for order flow test
        cls.buyer_1 = cls.env["res.partner"].create({"name": "MAWAT"})
        cls.buyer_2 = cls.env["res.partner"].create({"name": "TAWAM"})
        cls.property = cls.env["estate.property"].create({"name": "Test House", "expected_price": 100000.0})

    def test_offer_flow(self):
        """Test creating two offers and accepting one."""

        # Create two offers
        self.env["estate.property.offer"].create({"property_id": self.property.id, "partner_id": self.buyer_1.id, "price": 90000.0})
        offer_2 = self.env["estate.property.offer"].create({"property_id": self.property.id, "partner_id": self.buyer_2.id, "price": 95000.0})

        # Assert property passed in state "offer_received"
        self.assertRecordValues(self.property, [{"state": "offer_received"}])

        offer_2.accept_offer()

        # Assert property passed in state "offer_received"
        self.assertRecordValues(offer_2, [{"status": "accepted"}])
        self.assertRecordValues(self.property, [{"state": "offer_accepted", "selling_price": 95000.0, "buyer": self.buyer_2.id}])
