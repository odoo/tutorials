from odoo.tests.common import TransactionCase


class TestEstateProperty(TransactionCase):
    def test_salesperson(self):
        Allproperty = self.env["estate.property"]
        prop = Allproperty.create(
            {
                "name": "Test Property",
                "expected_price": 1000,
                "state": "new",
            }
        )
        self.assertEqual(prop.seller_id.id, self.env.user.id)
