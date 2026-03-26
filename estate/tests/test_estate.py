from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        """This runs once to set up the data for all tests in this class."""
        super().setUpClass()

        cls.type_id = cls.env.ref('estate.estate_property_type_residential')

        cls.property = cls.env['estate.property'].create({
            'name': 'Test Villa',
            'property_type_id': cls.type_id.id,
            'expected_price': 100000,
            'state': 'new',
        })

        cls.buyer = cls.env['res.partner'].create({'name': 'John Doe'})

    def test_01_create_offer_on_restricted_states(self):
        """Test: Cannot create offer if property is sold or canceled"""
        for restricted_state in ['sold', 'canceled', 'offer_accepted']:
            self.property.state = restricted_state

            with self.assertRaises(ValidationError, msg=f"Should fail on {restricted_state}"):
                self.env['estate.property.offer'].create({
                    'property_id': self.property.id,
                    'price': 50000,
                    'partner_id': self.buyer.id,
                })

    def test_02_sell_without_accepted_offer(self):
        """Test: Cannot sell property if no offers are 'accepted'"""
        self.property.state = 'new'
        with self.assertRaises(ValidationError):
            self.property.action_mark_as_sold()

    def test_03_successful_sell_flow(self):
        """Test: Property marks as 'sold' correctly when an offer is accepted"""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 90000,
            'partner_id': self.buyer.id,
        })

        offer.action_accept_offer()

        self.property.action_mark_as_sold()

        self.assertEqual(self.property.state, 'sold', "The property should be in 'sold' state.")
