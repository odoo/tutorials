from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.form import Form


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties = cls.env['estate.property'].create([
            {'name': 'property1', 'expected_price': 1000},
            {'name': 'property2', 'expected_price': 10000, 'garden': True, 'garden_area': 40},
        ])

        cls.property = cls.properties[0]
        cls.property_with_garden = cls.properties[1]

        cls.partner = cls.env['res.partner'].create({'name': 'partner1'})

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
           {'total_area': 20},
           {'total_area': 60},
        ])

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""

        # Cannot sell property with no offer
        with self.assertRaises(UserError):
            self.properties.action_sell_property()

        offers = self.env['estate.property.offer'].create([
            {'price': 2000, 'partner_id': self.partner.id, 'property_id': self.property.id},
            {'price': 10000, 'partner_id': self.partner.id, 'property_id': self.property_with_garden.id},
        ])

        offers.action_accept_offer()

        self.properties.action_sell_property()

        self.assertRecordValues(self.properties, [
           {'state': 'sold', 'selling_price': 2000},
           {'state': 'sold', 'selling_price': 10000},
        ])

        # Cannot cancel sold properties
        with self.assertRaises(UserError):
            self.properties.action_cancel_property()

    def test_action_cancel(self):
        """Test that everything behaves like it should when cancelling a property."""
        self.properties.action_cancel_property()
        self.assertRecordValues(self.properties, [
            {'state': 'cancelled'},
            {'state': 'cancelled'},
        ])

        # Cannot sell cancelled properties
        with self.assertRaises(UserError):
            self.properties.action_sell_property()

    def test_offer_creation(self):
        """
        Test that everything behaves like it should when creating an offer.
        - The user can create one or several offers for a property
        - The user can not sell properties with no accepted offers
        - The user can sell properties with an accepted offer
        - Offers can't be created for sold properties
        """
        offers = self.env['estate.property.offer'].create([
            {'price': 2000, 'partner_id': self.partner.id, 'property_id': self.property.id},
            {'price': 1500, 'partner_id': self.partner.id, 'property_id': self.property.id},
            {'price': 12200, 'partner_id': self.partner.id, 'property_id': self.property_with_garden.id},
        ])

        # Cannot sell property with no accepted offer
        with self.assertRaises(UserError):
            self.properties.action_sell_property()

        offers[0].action_accept_offer()
        offers[2].action_accept_offer()

        self.properties.action_sell_property()

        # Cannot create offer on sold property
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([
                {'price': 2000, 'partner_id': self.partner.id, 'property_id': self.property.id},
                {'price': 8500, 'partner_id': self.partner.id, 'property_id': self.property_with_garden.id},
            ])

    def test_garden_reset(self):
        """Test that the garden area and orientation correctly reset when garden is set to False in a form"""
        with Form(self.property) as property:
            property.garden = True

        self.assertRecordValues(self.property, [
            {'name': 'property1', 'garden': True, 'garden_area': 10, 'garden_orientation': 'north'},
        ])

        with Form(self.property) as property:
            property.garden = False

        self.assertRecordValues(self.property, [
            {'name': 'property1', 'garden': False, 'garden_area': 0, 'garden_orientation': None},
        ])
