from odoo.tests import TransactionCase


class TestEstateCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # PARTNER
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner'
        })

        # PROPERTIES
        cls.property_offer_received = cls.env['estate.property'].create({
            'name': 'Test Property Offer Received',
            'expected_price': 100000,
            'state': 'offer_received'
        })
        cls.property_offer_accepted = cls.env['estate.property'].create({
            'name': 'Test Property Offer Accepted',
            'expected_price': 200000,
            'state': 'offer_accepted'
        })
        cls.property_cancelled = cls.env['estate.property'].create({
            'name': 'Test Property Cancelled',
            'expected_price': 200000,
            'state': 'cancelled'
        })

        # OFFERS
        cls.offer = cls.env['estate.property.offer'].create({
            'property_id': cls.property_offer_received.id,
            'partner_id': cls.partner.id,
            'price': 110000
        })
        cls.offer_accepted = cls.env['estate.property.offer'].create({
            'property_id': cls.property_offer_accepted.id,
            'partner_id': cls.partner.id,
            'price': 220000,
            'status': 'accepted'
        })
