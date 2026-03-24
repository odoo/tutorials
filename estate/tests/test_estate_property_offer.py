from odoo.addons.estate.tests.common import EstateTestCommon
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstatePropertyOfferTestCase(EstateTestCommon):
    def test_stop_offer_creation_on_sold_property(self):
        estate_property = self.create_property('sold')

        with self.assertRaises(UserError):
            self.create_offer(estate_property, 50000)

    def test_offer_price_too_low_compared_to_other_offers(self):
        estate_property = self.create_property('offer_received')

        with self.assertRaises(UserError):
            self.create_offer(estate_property, 0)

    def test_offer_price_too_low_compared_to_expected_price(self):
        estate_property = self.create_property('new')
        offer = self.create_offer(estate_property, -estate_property.expected_price / 2)

        with self.assertRaises(UserError):
            offer.action_mark_as_accepted()
            estate_property.action_mark_as_sold()
