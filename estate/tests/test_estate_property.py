from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.EstateProperty = cls.env['estate.property']
        cls.EstatePropertyType = cls.env['estate.property.type']
        cls.EstatePropertyTag = cls.env['estate.property.tag']

    def test_offer_creation_sold_property(self):
        """Test that an offer cannot be created on a sold property."""
        sold_property = self.EstateProperty.create({
            'name': 'Test Property',
            'expected_price': 100000,
            'selling_price': 100000,
            'state': 'sold',
        })

        with self.assertRaises(UserError, msg="You cannot make an offer on a sold property."):
            self.env['estate.property.offer'].create({
                'price': 900000,
                'partner_id': self.env['res.partner'].create({'name': 'Test Partner'}).id,
                'property_id': sold_property.id,
            })

    def test_sell_property_without_accepted_offer(self):
        """Test that a property cannot be sold without an accepted offer."""
        property_no_offer = self.EstateProperty.create({
            'name': 'Test Property',
            'expected_price': 100000,
            'state': 'offer_received',
        })

        property_refused_offer_only = self.EstateProperty.create({
            'name': 'Test Property 2',
            'expected_price': 100000,
            'state': 'offer_received',
        })
        self.env['estate.property.offer'].create({
            'price': 90000,
            'partner_id': self.env['res.partner'].create({'name': 'Test Partner'}).id,
            'property_id': property_refused_offer_only.id,
            'status': 'refused',
        })

        with self.assertRaises(UserError, msg="You cannot sell a property without an accepted offer."):
            property_no_offer.action_set_sold()
            property_refused_offer_only.action_set_sold()

        def test_garden_onchange(self):
            with Form(self.EstateProperty) as property_form:
                property_form.name = 'Test Property'
                property_form.expected_price = 100000
                property_form.garden = True
                self.assertEqual(property_form.garden_area, 10, "The garden area should be set to 10 when the garden is checked.")
                self.assertEqual(property_form.garden_orientation, 'north', "The garden orientation should be set to north when the garden is checked.")

                property_form.garden = False
                self.assertFalse(property_form.garden_area, "The garden area should be cleared when the garden is unchecked.")
                self.assertFalse(property_form.garden_orientation, "The garden orientation should be cleared when the garden is unchecked.")
