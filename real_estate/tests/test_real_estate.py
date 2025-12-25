# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Property = self.env['estate.property']
        self.Offer = self.env['estate.property.offers']

    def test_offer_cannot_be_created_on_sold_property(self):
        """Offers cannot be created for sold properties"""
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'partner@example.com',
        })
        prop = self.Property.create({
            'name': 'Sold Property',
            'state': 'sold',
            'expected_price': 90000
        })
        with self.assertRaises(UserError):
            self.Offer.create({
                'price': 100000,
                'property_id': prop.id,
                'partner_id': partner.id,
            })

    def test_cannot_mark_as_sold_without_accepted_offer(self):
        """Should raise error when trying to sell a property with no offers at all"""
        prop = self.Property.create({
            'name': 'No Offers Property',
            'expected_price': 120000,
        })
        with self.assertRaises(UserError):
            prop.action_sold()

    def test_onchange_garden_unchecked_resets_fields(self):
        """Garden area and orientation should reset when garden is unchecked"""
        form = Form(self.env['estate.property'])
        form.name = "Reset Garden Test"
        form.expected_price = 90000
        form.garden = True
        prop = form.save()

        self.assertEqual(prop.garden_area, 10)
        self.assertEqual(prop.garden_orientation, "north")

        form = Form(prop)
        form.garden = False
        self.assertEqual(form.garden_area, 0)
        self.assertFalse(form.garden_orientation)

        prop = form.save()
        self.assertFalse(prop.garden)
        self.assertEqual(prop.garden_area, 0)
        self.assertFalse(prop.garden_orientation)
