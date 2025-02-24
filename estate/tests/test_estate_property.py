from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        """Set up test data before running the test cases."""
        super(EstateTestCase, cls).setUpClass()
        
        # Create properties
        cls.property1 = cls.env['estate.property'].create({
            'name': "Classy Villa",
            'state': 'offer_accepted',
            'expected_price' : 1000000
        })
        cls.property2 = cls.env['estate.property'].create({
            'name': "Modern Apartment",
            'state': 'offer_accepted',
            'expected_price' : 2000000
        })

        # Create offers
        cls.offer1 = cls.env['estate.property.offer'].create({
            'property_id': cls.property1.id,
            'price': 500000,
            'status': 'accepted',
            'partner_id' : cls.env['res.partner'].search([], limit=1).id
        })
        cls.offer2 = cls.env['estate.property.offer'].create({
            'property_id': cls.property2.id,
            'price': 600000,
            'status': 'accepted',
            'partner_id' : cls.env['res.partner'].search([], limit=1).id
        })

    def test_cannot_create_offer_for_sold_property(self):
        """Test that an offer cannot be created for a sold property."""
        self.property1.state = 'sold'
        with self.assertRaises(ValidationError):
            self.env['estate.property.offer'].create({
                'property_id': self.property1.id,
                'price': 700000,
                'status': 'accepted',
                'partner_id' : self.env['res.partner'].search([], limit=1).id
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        """Test that a property cannot be sold if no offer is accepted."""
        with self.assertRaises(UserError):
            self.property1.action_sold()
    def test_property_is_marked_as_sold_correctly(self):
        """Test that selling a property with an accepted offer updates the state."""
        self.offer1.status = 'accepted'
        self.property1.state = 'offer_accepted'
        self.property1.action_sold()
        self.assertEqual(self.property1.state, 'sold', "The property should be marked as sold.")

    def test_action_sell(self):
        """Test that everything behaves correctly when selling a property."""
        self.offer2.status = 'accepted'
        self.property2.state = 'offer_accepted'
        self.property2.action_sold()
        self.assertRecordValues(self.property2, [
            {'name': "Modern Apartment", 'state': 'sold'}
        ])

        with self.assertRaises(UserError):
            self.property2.action_sold()
