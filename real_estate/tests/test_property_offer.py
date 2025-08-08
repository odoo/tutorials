# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestPropertyOffer(TransactionCase):
    def test_property_offer_sold(self):
        user = self.env['res.partner'].create({
            'name': 'partner',
            'company_id': False,
        })
        property = self.env['estate.properties'].create(
            {'name': 'Test', 'state': 'sold', 'expected_price': 10000.00})
        with self.assertRaises(ValidationError):
            self.env['estate.properties.offer'].create({
                'property_id': property.id,
                'price': 1000000.00,
                'partner_id': user.id,
            })
