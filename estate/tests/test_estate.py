from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import UserError
from odoo.tests import Form


@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestEstate, cls).setUpClass()
        cls.property_new = cls.env['estate.property'].create({
            'name': 'Property 1',
            'expected_price': 100,
            'state': 'new'
        })
        cls.property_sold = cls.env['estate.property'].create({
            'name': 'Property 1',
            'expected_price': 100,
            'state': 'sold'
        })

    def test_create_offer(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 100,
                'partner_id': 1,
                'property_id': self.property_sold.id
            })

    def test_action_set_sold_no_offer(self):
        with self.assertRaises(UserError):
            self.property_sold.action_set_sold()

    def test_on_change_garden(self):
        f = Form(self.env['estate.property'])

        f.garden = True
        self.assertEqual(f.garden_area, 10)
        self.assertEqual(f.garden_orientation, 'north')

        f.garden = False
        self.assertEqual(f.garden_area, 0)
        self.assertEqual(f.garden_orientation, False)
