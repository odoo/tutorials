from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Property 1',
                'expected_price': 100,
            },
            {
                'name': 'Property 2',
                'expected_price': 200,
                'state': 'sold',
            },
            {
                'name': 'Property 3',
                'expected_price': 300,
                'state': 'sold',
            },
        ])

        cls.offer_partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })

    def test_cannot_create_offer_on_sold_property(self):
        """Test that we cannot create an offer on a sold property."""
        self.properties[0].write({'state': 'sold'})

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([{
                'price': 300,
                'partner_id': self.offer_partner.id,
                'property_id': self.properties[0].id,
            }])

    def test_cannot_sold_a_property_without_accepted_offer(self):
        """Test that we cannot sold a property without an accepted offer."""

        # Add an offer but not accept it
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([{
                'price': 300,
                'partner_id': self.offer_partner.id,
                'property_id': self.properties[1].id,
            }])
        # Sold without any offer
        with self.assertRaises(UserError):
            self.properties[2].action_sold()

    def test_rest_garden_fields(self):
        """Test that the garden fields are reset when the garden field is set to False."""
        property_record = self.properties[0]

        with Form(property_record) as property_form:
            property_form.garden = True
        self.assertEqual(property_record.garden_area, 10)
        self.assertEqual(property_record.garden_orientation, 'north')

        with Form(property_record) as property_form:
            property_form.garden = False
        self.assertEqual(property_record.garden_area, 0)
        self.assertFalse(property_record.garden_orientation)
