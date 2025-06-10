from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create([{'name': 'test_house'}])
        cls.partner = cls.env['res.partner'].create([{
            'id': 'test_partner',
            'name': 'test_person',
            'company_name': 'test_company',
            'street': 'test_street',
            'city': 'test_city',
            'zip': '12345',
            'country_id': cls.env.ref('base.us').id,
            'state_id': cls.env.ref('base.state_us_39').id,
            'phone': '+1 555-555-5555',
            'email': 'test@testing.example.com',
            'tz': 'Europe/Brussels',
        }])

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.properties.garden = True
        self.properties.garden_area = 15
        self.properties.garden_orientation = 'north'

        self.assertRecordValues(self.properties, [
           {'total_area': 35},
        ])

    def test_action_sell_without_accepted_offer(self):
        """Test that everything behaves like it should when selling an invalid property."""

        self.assertRecordValues(self.properties, [
           {'state': 'new'},
        ])

        with self.assertRaises(UserError):
            self.properties.action_property_sold()

    def test_action_sell_with_accepted_offer(self):
        """Test that everything behaves like it should when selling a valid property."""

        self.properties.offer_ids.create({
            'property_id': self.properties.id,
            'partner_id': self.partner.id,
            'price': 124,
            'validity': 14,
        })
        self.properties.offer_ids.action_offer_accept()
        self.properties.action_property_sold()

        self.assertRecordValues(self.properties, [
           {'state': 'sold'},
        ])

    def test_creation_offer_for_sold_property(self):
        """Test that everything behaves like it should when property is sold."""

        self.properties.offer_ids.create({
            'property_id': self.properties.id,
            'partner_id': self.partner.id,
            'price': 124,
            'validity': 14,
        })
        self.properties.offer_ids.action_offer_accept()
        self.properties.action_property_sold()

        with self.assertRaises(UserError):
            self.properties.offer_ids.create({
                'property_id': self.properties.id,
                'partner_id': self.partner.id,
                'price': 130,
                'validity': 14,
            })

    def test_enable_garden(self):
        """Test that default values are assigned to garden area and orientation when garden is enabled"""

        form = Form(self.env['estate.property'])
        form.garden = True

        self.assertEqual(form.garden_area, 10)
        self.assertEqual(form.garden_orientation, 'north')

    def test_disable_garden(self):
        """Test that values are removed from garden area and orientation when garden is disabled"""

        form = Form(self.env['estate.property'])
        form.garden = True
        form.garden_area = 15
        form.garden_orientation = 'south'
        form.garden = False

        self.assertEqual(form.garden_area, 0)
        self.assertEqual(form.garden_orientation, False)
