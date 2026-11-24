from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, TransactionCase
from odoo.tools import mute_logger

class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property_type = cls.env['estate.property.type'].create({
            'name': 'Test Property Type'
        })
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property 1',
            'property_type_id': cls.property_type.id,
            'expected_price': 100000,
        })
        cls.partner = cls.env['res.partner'].create({'name': 'Test Partner'})

    def test_accept_offer_no_buyer_or_selling_price(self):
        """Test that accepting an offer without a buyer or price raises UserError."""
        invalid_offers = [
            ('missing buyer', {'price': 100000, 'partner_id': False}),
            ('missing price', {'price': 0, 'partner_id': self.partner.id}),
            ('missing both buyer and price', {'price': 0, 'partner_id': False})
        ]

        for label, vals in invalid_offers:
            with self.subTest(case=label):
                offer = self.env['estate.property.offer'].new({ #testing .new
                    'property_id': self.property.id,
                    **vals,
                })
                with self.assertRaises(UserError):
                    offer.action_accept_offer()

    def test_refuse_offer_no_buyer_or_selling_price(self): # "duplicate" code is fine in unit tests
        """Test that accepting an offer without a buyer or price raises UserError."""
        invalid_offers = [
            ('missing buyer', {'price': 100000, 'partner_id': False}),
            ('missing price', {'price': 0, 'partner_id': self.partner.id}),
            ('missing both buyer and price', {'price': 0, 'partner_id': False})
        ]
        for label, vals in invalid_offers:
            with self.subTest(case=label):
                offer = self.env['estate.property.offer'].new({ #testing .new
                    'property_id': self.property.id,
                    **vals,
                })
                with self.assertRaises(UserError): # I consider that a UserError ought to be raised when refusing an incomplete offer
                    offer.action_refuse_offer()
