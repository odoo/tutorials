from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('estate', 'post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create property type
        cls.p_types = cls.env['estate.property.type'].create([
            {'name': 'House'},
            {'name': 'Studio'}
        ])

        # Create property tag
        cls.p_tags = cls.env['estate.property.tag'].create([
            {'name': 'Fantastic'},
            {'name': 'Dark', 'color': 1}
        ])

        # Create property
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Test Property',
                'expected_price': 123,
                'status': 'new',
                'property_type_id': cls.p_types[0].id,
                'property_tag_ids': cls.p_tags.mapped('id')
            }
        ])

        cls.test_partner = cls.env['res.partner'].create({
            'city': 'OrigCity',
            'name': 'TestingPartner',
        })

    def test_total_area(self):
        """Test that the total area is well computed"""
        property_0 = self.properties[0]

        property_0.living_area = 20

        self.assertEqual(property_0.total_area, property_0.living_area)

        property_0.garden_area = 30

        self.assertEqual(property_0.total_area, property_0.living_area + property_0.garden_area)

    def test_create_offer_sold_property(self):
        """Test that is forbidden to create an offer to a sold property"""
        property_0 = self.properties[0]

        property_0.status = 'sold'

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([
                {
                    'price': 123,
                    'property_id': property_0.id,
                    'partner_id': self.test_partner.id
                }
            ])

    def test_action_sell_no_accepted_offers(self):
        """Test that is forbidden to sell a property with no accepted offers"""
        property_0 = self.properties[0]

        offer = self.env['estate.property.offer'].create([
            {
                'price': 123,
                'property_id': property_0.id,
                'partner_id': self.test_partner.id
            }
        ])

        with self.assertRaises(UserError):
            property_0.action_set_status_sold()

        # Happy path
        offer.action_accept_offer()
        property_0.action_set_status_sold()

    def test_reset_fields_on_uncheck_garden(self):
        property_form = Form(self.env['estate.property'])

        property_form.garden = True
        # Fields should be visible and filled with default values
        self.assertEqual(property_form._get_modifier('garden_area', 'invisible'), False)
        self.assertEqual(property_form._get_modifier('garden_orientation', 'invisible'), False)
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, 'north')

        property_form.garden = False
        # Fields should be invisible and filled with reset values
        self.assertEqual(property_form.garden_area, 0)
        self.assertEqual(property_form.garden_orientation, False)
        self.assertEqual(property_form._get_modifier('garden_area', 'invisible'), True)
        self.assertEqual(property_form._get_modifier('garden_orientation', 'invisible'), True)
