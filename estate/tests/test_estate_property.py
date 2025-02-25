from odoo import Command
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.form import Form


@tagged("post_install", "-at_install")
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def SetUpClass(cls):
        super().SetUpClass()
        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "Antilia",
                    "expected_price": 10000,
                }
            ]
        )
        cls.offers = cls.env["estate.property.offer"].create(
            [
                {
                    "partner_id": cls.env.ref(xml_id="base.res_partner_12").id,
                    "property_id": cls.properties[0].id,
                    "price": 11999,
                }
            ]
        )

    def test_action_set_sold(self):
        """Test that you cannot sell a property without an accepted offer"""
        with self.assertRaises(UserError):
            self.properties.action_set_status_sold()
        self.offers[0].action_status_accepted()
        self.properties.action_set_status_sold()
        with self.assertRaises(UserError):
            self.properties[0].offer_ids = [
                Command.create(
                    {
                        "partner_id": self.env.ref(xml_id="base.res_partner_12").id,
                        "price": 10000,
                    }
                )
            ]

    def test_property_form(self):
        """Test the form view of properties."""
        with Form(self.properties[0]) as form:
            form.garden = True
            self.assertEqual(form.garden_area, 10)
            self.assertEqual(form.garden_orientation, "north")
            form.garden = False
            self.assertEqual(form.garden_area, 0, "The garden area should be 0")
            self.assertIs(
                form.garden_orientation, False, "The garden orientation should be False"
            )
