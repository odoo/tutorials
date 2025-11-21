from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create({'name': 'testAdd', 'expected_price': '190000'})
        cls.partner = cls.env['res.partner'].create({'name': 'eric'})

    def test_creation_estate(self):
        self.env['estate.property.offer'].create({'price': 180000, 'partner_id': self.partner.id, 'property_id': self.properties.id, 'status': 'accepted'})
        self.properties.state = 'sold'

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({'price': 180000, 'partner_id': self.partner.id, 'property_id': self.properties.id})

    def test_sell_property(self):
        self.properties.state = 'new'

        with self.assertRaises(UserError):
            self.properties.action_set_sold()

    def test_garden_onchange(self):
        property_form = Form(self.env['estate.property'])
        property_form.garden = True
        property_form.garden_area = 20
        property_form.garden_orientation = 'east'

        property_form.garden = False
        property_form.garden = True

        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, 'north')
