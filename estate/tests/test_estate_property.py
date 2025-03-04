from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    def test_sell_property_without_accepted_offer(self):
        estate_property = self.env['estate.property']

        property = estate_property.create({
            "name": "Test Property Without Offer",
            "expected_price": "100",
            "state": "new",
        })

        with self.assertRaises(ValidationError):
            property.action_sold()
