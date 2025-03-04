from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from datetime import timedelta

@tagged('post_install', '-at_install')
class TestEstatePropertyAuction(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['estate.property'].create({
            'name': 'Auction Property',
            'expected_price': 1000000,
            'property_sell_type': 'auction',
            'auction_end_time': fields.Datetime.now() + timedelta(hours=1),
        })
        cls.partner_a = cls.env['res.partner'].create({'name': 'Bidder A'})
        cls.partner_b = cls.env['res.partner'].create({'name': 'Bidder B'})

    def test_start_auction(self):
        """Test starting the auction."""
        self.property.action_start_property_auction()
        self.assertEqual(self.property.state, '02_auction', "Property should be in auction state.")

    def test_cannot_start_auction_twice(self):
        """Test that auction cannot be restarted."""
        self.property.action_start_property_auction()
        with self.assertRaises(UserError):
            self.property.action_start_property_auction()

    def test_cannot_start_auction_without_end_time(self):
        """Test auction cannot start without an end time."""
        self.property.auction_end_time = False
        with self.assertRaises(UserError):
            self.property.action_start_property_auction()

    def test_highest_bidder_computation(self):
        """Test that highest bidder is correctly determined."""
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner_a.id,
            'price': 1000000
        })
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner_b.id,
            'price': 2000000
        })
        self.assertEqual(self.property.highest_bidder, self.partner_b, "Highest bidder should be Bidder B.")

    def test_auto_accept_highest_bid(self):
        """Test that highest offer is auto-accepted when auction ends."""
        self.property.action_start_property_auction()

        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner_a.id,
            'price': 1000000
        })
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner_b.id,
            'price': 2000000
        })
        
        # Simulate auction end
        self.property.auction_end_time = fields.Datetime.now() - timedelta(minutes=1)
        self.env['estate.property']._check_auction_over()

        self.assertEqual(self.property.selling_price, 2000000, "Property should be sold at highest bid.")
        self.assertEqual(self.property.stage, 'sold', "Property stage should be sold.")
        self.assertEqual(self.property.state, '03_sold', "Property state should be sold.")

    def test_cannot_accept_offer_outside_auction(self):
        """Test that offers cannot be accepted before auction starts or after it's over."""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner_a.id,
            'price': 1000000
        })
        
        with self.assertRaises(UserError):
            offer.action_accept()

    def test_invoice_count(self):
        """Test that invoice count updates correctly."""
        self.env['account.move'].create({'property_id': self.property.id})
        self.env['account.move'].create({'property_id': self.property.id})
        
        self.assertEqual(self.property.invoice_count, 2, "Invoice count should be updated correctly.")

    def test_auction_resets_if_no_offers(self):
        """Test that if an auction ends with no offers, the property resets to template state."""
        self.property.auction_end_time = fields.Datetime.now() - timedelta(minutes=1)
        self.property._check_auction_over()

        self.assertEqual(self.property.state, '01_template', "Property should reset to template state if no offers were made.")

    def test_cannot_create_offer_below_expected_price_for_auction(self):
        """Test that an offer cannot be placed below the expected price for auction properties."""
        with self.assertRaises(UserError, msg="The offer price must be at least equal to the expected price."):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 400000  # Below expected price (500000)
            })

    def test_can_create_offer_at_or_above_expected_price_for_auction(self):
        """Test that an offer can be placed at or above the expected price for auction properties."""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner_a.id,
            'price': 1000000  # Exactly expected price
        })
        self.assertEqual(offer.price, 1000000, "Offer should be created successfully at expected price.")

        offer_high = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner_b.id,
            'price': 2000000  # Above expected price
        })
        self.assertEqual(offer_high.price, 2000000, "Offer should be created successfully above expected price.")
