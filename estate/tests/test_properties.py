from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstatePropertiesTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Test Property 1',
                'expected_price': 100000,
            },
            {
                'name': 'Test Property 2',
                'expected_price': 200000,
            },
        ])

    def test_sell_with_no_offer(self):
        with self.assertRaises(UserError):
            self.properties[0].action_set_sold()

    def test_sell_sets_sold(self):
        self.env['estate.property.offer'].create({
            'property_id': self.properties[1].id,
            'price': 210000,
            'partner_id': self.env['res.partner'].create({'name': 'Test Partner'}).id,
            'status': 'accepted',
        })
        self.properties[1].action_set_sold()
        self.assertEqual(self.properties[1].state, 'sold')

    def test_form_garden_defaults(self):
        property_form = Form(self.properties[0])
        property_form.garden = False
        self.assertEqual(property_form.garden_area, 0)
        self.assertEqual(property_form.garden_orientation, False)
        property_form.garden = True
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, 'north')
        property_form.garden = False
        self.assertEqual(property_form.garden_area, 0)
        self.assertEqual(property_form.garden_orientation, False)
