from odoo.tests.common import TransactionCase


class TestSalesman(TransactionCase):
    def test_some_action(self):
        self.env['estate.property'].sudo().create({
            'name': 'abc',
            'expected_price': 1000,
        })

        self.assertEqual(
            self.user_id.id,
            self.env.user.id
        )
