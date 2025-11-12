from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.partner=cls.env.ref('base.partner_demo')

        cls.property_type=cls.env['estate.property.type'].create({
            'name': 'Test Property Type'
        })

        cls.property=cls.env['estate.property'].create({
            'name': 'Test Property',
            'description': 'A beautiful test property for unit tests.',
            'living_area': 150,
            'garden': True,
            'garden_area': 50,
            'garden_orientation': 'east',
            'expected_price': 100000,
            'property_type_id': cls.property_type.id,
        })

        cls.property_with_accepted_offer=cls.env['estate.property'].create({
            'name': 'Test Property 2',
            'description': 'A beautiful test property for unit tests.',
            'living_area': 150,
            'garden': True,
            'garden_area': 50,
            'garden_orientation': 'east',
            'expected_price': 100000,
            'property_type_id': cls.property_type.id,
        })

        cls.property_new=cls.env['estate.property'].create({
            'name': 'Test Property 3',
            'description': 'A beautiful test property for unit tests.',
            'living_area': 150,
            'expected_price': 100000,
            'property_type_id': cls.property_type.id,
        })

        cls.accepted_offer=cls.env['estate.property.offer'].create({
            'property_id': cls.property_with_accepted_offer.id,
            'partner_id': cls.partner.id,
            'price': 95000,
        })
        cls.accepted_offer.action_accept()

        cls.new_offer=cls.env['estate.property.offer'].create({
            'property_id': cls.property_new.id,
            'partner_id': cls.env.ref('base.res_partner_12').id,
            'price': 110000,
        })

    def test_creation_area(self):
        """Test that the total_area is computed correctly."""
        self.property.living_area=150
        self.property.garden_area=50
        self.assertEqual(self.property.total_area, 200, "Total area should be 200")

    def test_action_sell(self):
        """Test that a property with accepted offer can be sold."""
        self.property_with_accepted_offer.action_sold()
        self.assertEqual(self.property_with_accepted_offer.status, 'sold',
                         "Property status should be 'sold' after selling")

    def test_action_sell_no_offer(self):
        """Test that a property cannot be sold if no accepted offers are present."""
        with self.assertRaises(UserError, msg="Should not be able to sell without accepted offer"):
            self.property.action_sold()

    def test_action_sell_cancelled_property(self):
        """Test that a cancelled property cannot be sold."""
        self.property_with_accepted_offer.action_cancel()
        with self.assertRaises(UserError, msg="Should not be able to sell cancelled property"):
            self.property_with_accepted_offer.action_sold()

    def test_action_create_offer_for_sold_property(self):
        """Test that action_accept fails on a sold property."""
        self.new_offer.action_accept()
        self.property_new.action_sold()
        new_offer=self.env['estate.property.offer'].create({
            'property_id': self.property_new.id,
            'partner_id': self.partner.id,
            'price': 120000,
        })
        with self.assertRaises(UserError, msg="Should not be able to accept offer for sold property"):
            new_offer.action_accept()

    def test_sell_property_correctly_marked_sold(self):
        """Test that selling a property with an accepted offer correctly marks it as sold."""
        self.property_with_accepted_offer.action_sold()
        self.assertEqual(self.property_with_accepted_offer.status, 'sold',
                         "Property status should be 'sold' after selling")

    def test_garden_area_reset_on_uncheck(self):
        """Ensure Garden Area and Orientation reset when the Garden checkbox is unchecked."""
        self.property.garden=True
        self.property.garden_area=100
        self.property.garden_orientation='north'
        self.property.garden=False
        self.property._onchange_garden()
        self.assertEqual(self.property.garden_area, 0, "Garden area should reset to 0")
        self.assertFalse(self.property.garden_orientation, "Garden orientation should reset to False")

    def test_best_price_calculation(self):
        """Test that best price is correctly calculated from offers."""
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner.id,
            'price': 90000,
        })
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner.id,
            'price': 105000,
        })
        self.assertEqual(self.property.best_price, 105000, "Best price should be the highest offer")

    def test_offer_price_validation(self):
        """Test that offers with price below best price are rejected."""
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner.id,
            'price': 110000,
        })
        with self.assertRaises(UserError, msg="Lower offers should be rejected"):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': self.partner.id,
                'price': 100000,
            })
