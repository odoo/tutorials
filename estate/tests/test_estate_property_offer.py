from datetime import datetime

from odoo.exceptions import UserError
from odoo.tests import Form, TransactionCase
from odoo.tests import freeze_time


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

    def test_minimal_fields_required_for_offer(self):
        new_property_offer = Form(self.env['estate.property.offer'])
        with self.assertRaises(AssertionError):
            new_property_offer.save()
        new_property_offer.partner_id = self.partner
        with self.assertRaises(AssertionError):
            new_property_offer.save()
        new_property_offer.property_id = self.property

    def test_accept_offer_no_buyer_or_selling_price(self):
        """Test that accepting an offer without a buyer or price raises UserError."""
        invalid_offers = [
            ('missing buyer', {'price': 100000, 'partner_id': False}),
            ('missing price', {'price': 0, 'partner_id': self.partner.id}),
            ('missing both buyer and price', {'price': 0, 'partner_id': False})
        ]

        for label, vals in invalid_offers:
            with self.subTest(case=label):
                offer = self.env['estate.property.offer'].new({  # testing .new
                    'property_id': self.property.id,
                    **vals,
                })
                with self.assertRaises(UserError):
                    offer.action_accept_offer()

    def test_refuse_offer_no_buyer_or_selling_price(self):  # "duplicate" code is fine in unit tests
        """Test that accepting an offer without a buyer or price raises UserError."""
        invalid_offers = [
            ('missing buyer', {'price': 100000, 'partner_id': False}),
            ('missing price', {'price': 0, 'partner_id': self.partner.id}),
            ('missing both buyer and price', {'price': 0, 'partner_id': False})
        ]
        for label, vals in invalid_offers:
            with self.subTest(case=label):
                offer = self.env['estate.property.offer'].new({  # testing .new
                    'property_id': self.property.id,
                    **vals,
                })
                with self.assertRaises(UserError):  # I consider that a UserError ought to be raised when refusing an incomplete offer
                    offer.action_refuse_offer()

    #  check that date_deadline and validity work as expected
    #  deadline defaults to 7 days (validity's default) after offer's creation date
    #  on validity change, deadline should change accordingly
    #  on deadline change, validity should change accordingly

    @freeze_time('2023-03-02')
    def test_deadline_and_validity(self):
        """given a creation date, deadline should default 7 days later.
        Changing deadline or deadline should change the other."""
        with Form(self.env['estate.property.offer']) as offer_form:
            offer_form.property_id = self.property
            offer_form.price = 100000
            offer_form.partner_id = self.partner
            self.assertEqual(offer_form.date_deadline, datetime(2023, 3, 9, 0, 0))
            offer_form.validity = 14
            self.assertEqual(offer_form.date_deadline, datetime(2023, 3, 16, 0, 0))
