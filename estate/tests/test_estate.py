# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.form import Form

@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env["estate.property"].create([{
            "name": "Sarthi Bunglow",
            "expected_price": 10000,
        }])
        cls.offers = cls.env["estate.property.offer"].create([{
            "partner_id": cls.env.ref(xml_id="base.res_partner_12").id,
            "property_id": cls.properties[0].id,
            "price": 11999,
        }])

    def test_action_sell_property(self):
        """Test that everything behaves like it should when selling a property."""
        # You cannot sell a property without an accepted offer
        with self.assertRaises(UserError):
            self.properties.action_sell_property()
        # Accept the offer
        self.offers[0].accept_offer()
        # Now you can sell it
        self.properties.action_sell_property()
        self.assertRecordValues(self.properties, [
            {"state": "sold"},
        ])
        # You cannot create an offer for a sold property
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create([{
                "partner_id": self.env.ref(xml_id="base.res_partner_12").id,
                "property_id": self.properties[0].id,
                "price": 10000,
            }])

    def test_property_form(self):
        """Test the form view of properties."""
        with Form(self.properties[0]) as prop:
            self.assertEqual(prop.garden_area, 0)
            self.assertIs(prop.garden_orientation, False)
            prop.garden = True
            self.assertEqual(prop.garden_area, 10)
            self.assertEqual(prop.garden_orientation, "north")
            prop.garden = False
            self.assertEqual(prop.garden_area, 0)
            self.assertIs(prop.garden_orientation, False)
