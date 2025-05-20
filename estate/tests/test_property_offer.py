from xml.dom import ValidationErr
from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env["estate.property"].create([
            {
                "name": "Sale Test Property",
                "description": "Test Description",
                "expected_price": 100000,
                "living_area": 50,
            },
            {
                "name": "Garden Test Property",
                "description": "Test Description Garden",
                "expected_price": 200000,
                "living_area": 100,
            },
        ])

        cls.offers = cls.env["estate.property.offer"].create([
            {
                "partner_id": cls.env.ref("base.res_partner_2").id,
                "price": 110000,
                "property_id": cls.properties[0].id,
            },
            {
                "partner_id": cls.env.ref("base.res_partner_12").id,
                "price": 130000,
                "property_id": cls.properties[0].id,
            },
            {
                "partner_id": cls.env.ref("base.res_partner_2").id,
                "price": 150000,
                "property_id": cls.properties[0].id,
            },
        ])

    def test_sell_property_without_accepted_offer(self):
        """
        Test selling a property without an accepted offer.
        Ensure that a UserError is raised when trying to sell a property without an accepted offer.
        Ensure that other offers are not allowed to be created after the property is sold.
        """
        with self.assertRaises(UserError):
            self.properties[0].action_sold()

        self.offers[1].action_accept()
        self.properties[0].action_sold()

        self.assertEqual(
            self.properties[0].state,
            "sold",
            "Property was not marked as sold"
        )

        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create({
                "partner_id": self.env.ref("base.res_partner_2").id,
                "price": 200000,
                "property_id": self.properties[0].id,
            })

    def test_garden_toggle(self):
        """
        Test toggling the garden field on a new property.
        Ensure that the garden area and orientation are reset properly.
        """
        property = self.env["estate.property"].new({
            "name": "Test Garden Property",
            "expected_price": 120000,
            "living_area": 60,
        })

        # Enable garden
        property.garden = True
        property._onchange_garden()

        self.assertEqual(property.garden_area, 10, "Garden area should be 10 when garden is enabled")
        self.assertEqual(property.garden_orientation, "North", "Orientation should be North when garden is enabled")

        # Disable garden
        property.garden = False
        property._onchange_garden()

        self.assertEqual(property.garden_area, 0, "Garden area should be 0 when garden is disabled")
        self.assertFalse(property.garden_orientation, "Orientation should be False when garden is disabled")
    
    def test_offer_price_must_be_positive(self):
        """
        Test that creating an offer with zero or negative price fails.
        """
        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create({
                "partner_id": self.env.ref("base.res_partner_2").id,
                "price": 0,
                "property_id": self.properties[1].id,
            })

