# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "Villa on the beach",
                    "expected_price": 1000000,
                    "living_area": 100,
                },
                {
                    "name": "Apartment in the city",
                    "expected_price": 500000,
                    "living_area": 50,
                },
            ]
        )

        cls.offer = cls.env["estate.property.offer"].create(
            {
                "partner_id": cls.env.ref("base.res_partner_12").id,
                "property_id": cls.properties[0].id,
                "price": 1000000,
                "status": "accepted",
            }
        )

        cls.properties[0].offer_ids = [(6, 0, [cls.offer.id])]

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.assertRecordValues(
            self.properties,
            [
                {
                    "name": "Villa on the beach",
                    "expected_price": 1000000,
                    "total_area": 100,
                },
                {
                    "name": "Apartment in the city",
                    "expected_price": 500000,
                    "total_area": 50,
                },
            ],
        )

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.properties[0].action_set_property_sold()
        self.assertEqual(self.properties[0].state, "sold")

    def test_create_offer_for_sold_property(self):
        """Test that no new offer can be created for a property once it's sold."""
        self.properties[0].action_set_property_sold()
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "partner_id": self.env.ref("base.res_partner_12").id,
                    "property_id": self.properties[0].id,
                    "price": 1000000,
                }
            )

    def test_sold_property_without_offer(self):
        """Test that a property cannot be sold without an accepted offer."""
        with self.assertRaises(UserError):
            self.properties[1].action_set_property_sold()

    def test_is_garden_checkbox(self):
        """Test that the garden area and orientation reset to default values when the garden checkbox is unchecked."""
        property_form = Form(self.properties[0])

        self.assertFalse(property_form.garden)

        property_form.garden = True
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, "north")

        property_form.garden_area = 100
        property_form.garden_orientation = "east"
        property_form.save()

        self.assertEqual(property_form.garden_area, 100)
        self.assertEqual(property_form.garden_orientation, "east")

        property_form.garden = False
        property_form.save()

        property_form.garden = True
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, "north")
