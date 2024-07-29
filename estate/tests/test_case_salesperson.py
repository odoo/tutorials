from odoo.tests.common import TransactionCase


class Testestateproperty(TransactionCase):
    def test_case_salesperson(self):
        estate_property = self.env["estate.property"]
        properties = estate_property.create(
            {
                "name": "Test_estate_property",
                "expected_price": "130000",
                "state": "new",
            }
        )
        self.assertEqual(properties.salesperson_id.id, self.env.user.id)
        # self.assertEqual(2 + 3, 6)
