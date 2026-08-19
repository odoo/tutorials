from odoo.tests import TransactionCase


class TestEstateCommon(TransactionCase):
    def setUp(self):
        super().setUp()

        self.property = self.env["estate.property"].create(
            {
                "name": "House 1",
                "expected_price": 1000,
                "property_type_id": self.env["estate.type"]
                .create({"name": "House"})
                .id,
                "seller_id": self.env.user.id,
            }
        )
