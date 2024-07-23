from odoo.tests.common import TransactionCase


class TestSalesPerson(TransactionCase):
    def test_sales_person_user(self):
        record = self.env['estate.property'].sudo().create({
            'name': 'test',
            'expected_price': 1234
        })
        self.assertEqual(record.sales_person.id, self.env.user.id)
