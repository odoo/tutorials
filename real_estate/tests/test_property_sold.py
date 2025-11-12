# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestPropertySold(TransactionCase):
    def test_property_offer_sold(self):
        property = self.env['estate.properties'].create(
            {'name': 'Test', 'state': 'offer_accepted', 'expected_price': 10000.00})
        with self.assertRaises(ValidationError):
            property.action_property_sold()
