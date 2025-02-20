# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "Property1",
                    "living_area": 100,
                    "expected_price": 10000,
                },
                {
                    "name": "Property2",
                    "living_area": 20,
                    "expected_price": 4000,
                },
            ]
        )

        cls.offers = cls.env["estate.property.offer"].create({
            'partner_id': cls.env.ref('base.res_partner_10').id,
            'property_id': cls.properties[0].id,
            'price': 1000000,
            'status': 'accepted'
        })

        cls.properties[0].offer_ids = [(6, 0, [cls.offers.id])]

    def test_creation_area(self):
        self.assertRecordValues(
            self.properties,
            [
                {
                    "name": "Property1",
                    "total_area": 100,
                    "expected_price": 10000,
                },
                {
                    "name": "Property2",
                    "total_area": 20,
                    "expected_price": 4000,
                },
            ],
        )

    def test_sell_property(self):
        self.properties[0].action_sold()
        self.assertEqual(self.properties[0].state, "sold")

    def test_sell_property_without_offer(self):
        with self.assertRaises(UserError):
            self.properties[1].action_sold()

    def test_check_offer_for_sold_property(self):
        self.properties[0].action_sold()
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "partner_id": self.env.ref("base.res_partner_10").id,
                    "property_id": self.properties[0].id,
                    "price": 10000,
                }
            )

    def test_garden_checkbox_area_orientation(self):
        property = Form(self.properties[0])
        self.assertFalse(property.garden)
        property.garden = True
        self.assertEqual(property.garden_orientation, 'north')
        self.assertEqual(property.garden_area, 10)
        property.garden_orientation = 'east'
        property.garden_area = 100
        property.save()
        self.assertEqual(property.garden_orientation, 'east')
        self.assertEqual(property.garden_area, 100)
        property.garden = False
        property.save()
        property.garden = True
        self.assertEqual(property.garden_orientation, 'north')
        self.assertEqual(property.garden_area, 10)
