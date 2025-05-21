from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests import Form


@tagged('post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['estate.property'].create(
            {'name': 'Test property', "expected_price": 10},
        )

    def test_new_offer_cannot_be_lower_than_others(self):
        """Test that an offer cannot be created for a sold property"""
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': 1,
            'status': 'accepted',
            'price': 10,
        }),

        with self.assertRaises(UserError) as cm:
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': 1,
                'price': 2,
            })

    def test_sell_property_without_accepted_offers(self):
        """Test that a property cannot be sold without any accepted offers"""
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': 1,
            'price': 10,
        })

        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': 1,
            'price': 20,
        })

        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_property_state_after_sale(self):
        """Test that the property state is 'sold' after the sale"""
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': 1,
            'status': 'accepted',
            'price': 10,
        })


        self.property.action_set_sold()
        self.assertTrue(self.property.state == 'sold')

    def test_garden_set_to_true(self):
        self.property.garden = False
        with Form(self.property) as property_form:
            property_form.garden = True

        self.assertRecordValues(self.property, [
            {'garden_area': 10, 'garden_orientation': 'north'}
        ])

    def test_garden_set_to_false(self):
        self.property.garden = True
        self.property.garden_area = 10
        self.property.garden_orientation = 'north'
        with Form(self.property) as property_form:
            property_form.garden = False

        self.assertFalse(self.property.garden_area)
        self.assertEqual(self.property.garden_area, 0)
