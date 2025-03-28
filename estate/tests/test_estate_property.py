from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'PropertyA',
                'expected_price': 1000,
                'garden': True,
                'garden_area': 100,
                'living_area': 100,
            },
            {
                'name': 'PropertyB',
                'expected_price': 1000,
                'garden': True,
                'garden_area': 0,
                'living_area': 0,
            },
            {
                'name': 'PropertyC',
                'expected_price': 1000,
                'garden': True,
                'garden_area': 999,
                'living_area': 555,
            }
        ])
        cls.partner = cls.env['res.partner'].create([
            {
                'name': 'Some Company',
                'is_company': True,
            },
            {
                'name': 'Other Company',
                'is_company': True,
            },
        ])

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        for index, property in enumerate(self.properties):
            self.assertRecordValues(property, [
                {'total_area': property.garden_area + property.living_area},
            ])

    def test_create_offer_on_property(self):
        """Test that creating an offer on a sold property is not possible."""
        self.properties[0].state = 'new'
        self.env['estate.property.offer'].create({
            'partner_id': self.partner[0].id,
            'price': self.properties[0].expected_price,
            'property_id': self.properties[0].id
        }).action_accept_offer()

        self.properties[0].action_mark_sold()
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'partner_id': self.partner[1].id,
                'price': self.properties[0].expected_price * 2,
                'property_id': self.properties[0].id
            })

    def test_mark_property_as_sold(self):
        """Test that selling a property with no accepted offer is not possible."""
        with self.assertRaises(UserError):
            self.properties[1].action_mark_sold()

        self.env['estate.property.offer'].create({
            'partner_id': self.partner[0].id,
            'price': self.properties[1].expected_price,
            'property_id': self.properties[1].id
        }).action_accept_offer()
        self.properties[1].action_mark_sold()

    def test_garden_toggle_resets_data(self):
        """Test that toggling garden resets garden_area and garden_orientation."""
        with Form(self.properties[2]) as form:
            form.garden = False
            form.save()
            self.assertEqual(self.properties[2].garden_area, 0)
            self.assertEqual(self.properties[2].garden_orientation, False)
            form.garden = True
            form.save()
            self.assertEqual(self.properties[2].garden_area, 10)
            self.assertEqual(self.properties[2].garden_orientation, 'north')
