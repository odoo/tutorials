from odoo.tests.common import TransactionCase


class TestProperty(TransactionCase):
    def test_case(self):
        Pro = self.env["estate.property"]
        prop = Pro.create(
            {
                "name": "Test Property",
                "expected_price": 1000,
                "state": "new",
            }
        )
        self.assertEqual(prop.seller_id.id, self.env.user.id)
