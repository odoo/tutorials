from odoo.tests import TransactionCase, tagged
from datetime import datetime, timedelta
from odoo import fields


@tagged('standard')
class TestAwesomeEstateOffer(TransactionCase):
    """Test offer-specific business logic: suspicious, deadlines, etc."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Property = cls.env['awesome.estate.property']
        cls.Offer = cls.env['awesome.estate.property.offer']
        cls.Partner = cls.env['res.partner']

        cls.partner_a = cls.Partner.create({'name': 'Buyer A'})
        cls.partner_b = cls.Partner.create({'name': 'Buyer B'})

        cls.property = cls.Property.create(
            {
                'name': 'Offer Test Property',
                'expected_price': 300000,
                'living_area': 100,
            }
        )
        cls.property_b = cls.Property.create(
            {
                'name': 'Second Property',
                'expected_price': 200000,
                'living_area': 80,
            }
        )

    def test_offer_creation_sets_property_state(self):
        self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        self.assertEqual(self.property.state, 'offer_received')

    def test_offer_default_validity(self):
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        self.assertEqual(offer.validity, 7)

    def test_offer_date_deadline_compute(self):
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        self.assertTrue(offer.date_deadline)

    def test_offer_refuse(self):
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        offer.action_refuse()
        self.assertEqual(offer.status, 'refused')

    def test_accept_refuses_other_offers(self):
        offer_a = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        offer_b = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_b.id,
                'price': 290000,
            }
        )
        offer_b.action_accept()
        self.assertEqual(offer_b.status, 'accepted')
        self.assertEqual(offer_a.status, 'refused')

    def test_cannot_accept_suspicious_offer(self):
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        offer.is_suspicious = True
        with self.assertRaises(Exception):
            offer.action_accept()

    def test_mark_suspicious_clear(self):
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        offer.action_mark_suspicious()
        self.assertTrue(offer.is_suspicious)
        offer.action_clear_suspicious()
        self.assertFalse(offer.is_suspicious)

    def test_same_partner_duplicate_flagged(self):
        """Two offers by same partner within 5 min on same property = suspicious."""
        offer1 = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        offer2 = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 290000,
            }
        )
        self.assertTrue(offer1.is_suspicious)
        self.assertTrue(offer2.is_suspicious)

    def test_different_partner_not_suspicious(self):
        """Offers from different partners should not be flagged."""
        offer1 = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        offer2 = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_b.id,
                'price': 290000,
            }
        )
        self.assertFalse(offer1.is_suspicious)
        self.assertFalse(offer2.is_suspicious)

    def test_same_partner_diff_property_not_suspicious(self):
        """Same partner, different property — not suspicious."""
        offer1 = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 280000,
            }
        )
        offer2 = self.Offer.create(
            {
                'property_id': self.property_b.id,
                'partner_id': self.partner_a.id,
                'price': 180000,
            }
        )
        self.assertFalse(offer1.is_suspicious)
        self.assertFalse(offer2.is_suspicious)

    def test_cron_refuse_expired_offers(self):
        self.Offer._cron_refuse_expired_offers()
