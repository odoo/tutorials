from odoo.tests import tagged
from odoo.exceptions import UserError, ValidationError
from odoo.addons.estate.tests.common import TestEstateCommon


@tagged('post_install', '-at_install')
class TestEstatePropertyOffer(TestEstateCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_create_offer(self):
        # Test failed case: Property is already sold
        self.property_offer_accepted.action_sell_property()

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property_offer_accepted.id,
                'partner_id': self.partner.id,
                'price': 250000
            })

        # Test failed case: Offer price is less than maximum offer
        with self.assertRaises(ValidationError):
            self.env['estate.property.offer'].create({
                'property_id': self.property_offer_received.id,
                'partner_id': self.partner.id,
                'price': 90000  # Less than the expected price
            })

        # Test successful case
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property_offer_received.id,
            'partner_id': self.partner.id,
            'price': 120000  # Valid offer price
        })
        self.assertTrue(offer)
        self.assertEqual(offer.property_id, self.property_offer_received)
