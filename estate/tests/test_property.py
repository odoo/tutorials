from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        type = cls.env['estate.property.type'].search([('name', '=', 'Residential')], limit=1)
        cls.partner = cls.env['res.partner'].create({'name': 'Test Partner'})
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'New Villa',
                'property_type_id': type.id,
                'state': 'new',
                'expected_price': 100000,
                'living_area': 100,
            },
            {
                'name': 'Sold Villa',
                'property_type_id': type.id,
                'state': 'sold',
                'expected_price': 200000.00,
                'living_area': 200,
            }
        ])

    def test_create_offer_on_sold_property(self):
        sold = self.properties[1]
        with self.assertRaises(UserError):
            sold.offer_ids.create({
                'price': 150000,
                'partner_id': self.partner.id,
                'property_id': sold.id
            })

    def test_no_accepted_offer_sell(self):
        property = self.properties[0]
        with self.assertRaises(UserError):
            property.property_set_sold()
        property.offer_ids.create({
            'price': 100000,
            'partner_id': self.partner.id,
            'property_id': property.id
        })
        with self.assertRaises(UserError):
            property.property_set_sold()

    def test_selling_property(self):
        offer = self.properties[0].offer_ids.create({
            'price': 100000,
            'partner_id': self.partner.id,
            'property_id': self.properties[0].id
        })
        offer.offer_accept()
        self.properties[0].property_set_sold()
        self.assertEqual(self.properties[0].state, 'sold')

    def test_reset_garden_area_and_orientation(self):
        with Form(self.properties[0]) as property_form:
            property_form.garden = True
            self.assertEqual(property_form.garden_area, 10)
            self.assertEqual(property_form.garden_orientation, 'north')
            property_form.garden = False
            self.assertEqual(property_form.garden_area, 0)
            self.assertEqual(property_form.garden_orientation, False)
