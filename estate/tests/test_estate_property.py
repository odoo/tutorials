from odoo.tests.common import TransactionCase


class CreatePropertyTest(TransactionCase):

    def test_create_property(self):
        record = self.env['estate.property'].create({
            'name': 'ABCD',
            'expected_price': 10
        })
        self.assertEqual(record.user_id.id, self.env.user.id)
