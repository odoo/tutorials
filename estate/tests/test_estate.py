from odoo import Command
from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.tests import Form
from odoo.exceptions import UserError


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "Double Villa",
                    "expected_price": 10000,
                    "status": "new",
                }
            ]
        )
        # Create an offer for the property
        cls.offers = cls.env["estate.property.offer"].create(
            [
                {
                    "partner_id": cls.env.ref(xml_id="base.res_partner_12").id,
                    "property_id": cls.properties[0].id,
                    "price": 10000,  # Ensure the offer price is valid
                }
            ]
        )

    def test_action_sold(self):
        """Test that everything behaves like it should when selling a property."""
        # You cannot sell a property without an accepted offer
        with self.assertRaises(UserError):
            self.properties.action_sold()
        # Accept the offer
        self.offers[0].action_accepted()
        self.assertEqual(self.properties.status, "offer_accepted")
        # Now you can sell it
        self.properties.action_sold()
        self.assertEqual(self.properties.status, "sold")
        # You cannot create an offer for a sold property
        with self.assertRaises(UserError):
            self.properties[0].offer_ids = [
                Command.create(
                    {
                        "partner_id": self.env.ref(xml_id="base.res_partner_12").id,
                        "price": 140000,
                    },
                )
            ]

    def test_property_form(self):
        """Test the form view of properties."""
        with Form(self.properties[0]) as prop:
            self.assertEqual(prop.garden_area, 0)
            self.assertFalse(prop.garden_orientation)
            prop.garden = True
            self.assertEqual(prop.garden_area, 10)
            self.assertEqual(prop.garden_orientation, "north")
            prop.garden = False
            self.assertEqual(prop.garden_area, 0)
            self.assertFalse(prop.garden_orientation)
