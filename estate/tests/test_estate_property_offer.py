from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        """Create a partner"""
        cls.partner = cls.env['res.partner'].create([{
            'name': 'Test Partner',
        }])

        """Create a simple property"""
        cls.property = cls.env['estate.property'].create(
            [{
                'name': 'House on the beach',
                'expected_price': 100000,
                'postcode': 5000,
                'state': 'new'
            }])

        """Create a sold property"""
        cls.sold_property = cls.env['estate.property'].create(
            [{
                'name': 'Sold House in the woods',
                'expected_price': 100000,
                'postcode': 1000,
                'state': 'sold',
                'buyer_id': cls.partner.id,
                'selling_price': 120000,
            }]
        )

    def test_offer_create(self):
        """Create an offer for an available property"""
        offer1 = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner.id,
            'price': 100000,
        })

        # Check if the offer is listed in the proporty Offer list
        self.assertEqual(len(self.property.offer_ids), 1)
        self.assertEqual(self.property.offer_ids[0], offer1)

        """
        Check blocking of the creation of an offer
        for an sold property
        """
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.sold_property.id,
                'partner_id': self.partner.id,
                'price': 200000,
            })

    def test_offer_validation(self):
        """
        Test that offer can be created and accepted"""
        partner = self.env['res.partner'].create([{
            'name': 'Test Partner',
        }])

        """Create an offer with less 90% of the expected price"""
        offer1 = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': partner.id,
            'price': 50000
        })

        """Creating an offer with more than 90% of the expected price"""
        offer2 = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': partner.id,
            'price': 95000
        })

        """Check that the status of the property changed to 'offer_received'"""
        self.assertEqual(self.property.state, 'offer_received')

        """
        Try accepting the first offer with less than 90% of the expected price
        This should raise UserError
        """
        with self.assertRaises(UserError):
            offer1.action_accept_property_offer()

        """Accept the second offer"""
        offer2.action_accept_property_offer()

        """
        Check that the offer status is accepted &
        Check that the buyer_id is set on the property
        Check that the state is changed to 'offer_accepted'
        """
        self.assertEqual(offer2.status, 'accepted')
        self.assertEqual(self.property.state, 'offer_accepted')
        self.assertEqual(self.property.buyer_id, partner)
