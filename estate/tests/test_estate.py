# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):  # overridean method of TransactionCase class, used to create dummey data for testing.
        super(EstateTestCase, cls).setUpClass()
        cls.buyer = cls.env['res.partner'].create({
            'name': 'buyer'
        })
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 1000,
            'selling_price': 2000
        })
        cls.offer = cls.env['estate.property.offer'].create({
            'partner_id': cls.buyer.id,
            'property_id': cls.property.id,
            'price': 9000
        })


    def test_action_offer_accept(self):
        self.offer.action_offer_accept()
        with self.assertRaises(UserError, msg="Property with accepted offer able to accept another offer "):
            self.offer.action_offer_accept()

        for of in self.offer.property_id.offer_ids:
            if self.offer != of:
                self.assertEqual(of.status, "refused" ,msg="All other offers are not refused if you accept one offer")
            else:
                self.assertEqual(of.status, "accepted", msg="Accepted offer button is not accept offer correctly")


    def test_action_sold_property(self):
        self.offer.action_offer_accept()
        self.property.action_sold_property()
        self.assertRecordValues(self.property, [
            {'state': 'sold'},
        ])
        self.property.state = "cancelled"
        with self.assertRaises(UserError, msg="Cancelled property also sold"):
            self.property.action_sold_property()
        self.property.state = "offer received"
        self.offer.status = "refused"
        with self.assertRaises(UserError, msg="Property can sold without offer accepting"):
            self.property.action_sold_property()


    def test_garden_fom(self):
        with Form(self.property) as prop:
            self.assertEqual(prop.garden_area, 0, msg="check default value of garden_area")
            self.assertIs(prop.garden_orientation, False, msg="check default value of garden_orientation")

            prop.garden = True
            self.assertEqual(prop.garden_area, 10, msg="Garden is set, so default value would'nt work!")
            self.assertEqual(prop.garden_orientation, "north", msg="Garden is set, so default orientation is would'nt work!")

            prop.garden = False
            self.assertEqual(prop.garden_area, 0, msg="Garden is reset, default value would work!")
            self.assertIs(prop.garden_orientation, False, msg="check default value of garden_orientation")
