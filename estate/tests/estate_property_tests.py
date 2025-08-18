from odoo import Command  # noqa: F401
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests import Form, TransactionCase


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "Test Property",
                    "description": "Some Description",
                    "expected_price": 100000,
                    "living_area": 50,
                },
                {
                    "name": "Test Property Garden",
                    "description": "property with garden",
                    "expected_price": 200000,
                    "living_area": 100,
                },
            ]
        )

        cls.offers = cls.env["estate.property.offer"].create(
            [
                {
                    "partner_id": cls.env.ref("base.res_partner_2").id,
                    "price": 110000,
                    "property_id": cls.properties[0].id,
                },
                {
                    "partner_id": cls.env.ref("base.res_partner_1").id,
                    "price": 120000,
                    "property_id": cls.properties[0].id,
                },
                {
                    "partner_id": cls.env.ref("base.res_partner_3").id,
                    "price": 125000,
                    "property_id": cls.properties[0].id,
                },
            ]
        )

    def test_property_sale(self):
        with self.assertRaises(UserError):
            self.properties[0].action_set_sold()

        self.offers[1].action_accept_offer()

        self.properties[0].action_set_sold()
        self.assertEqual(self.properties[0].state, "sold", "Property was not sold")

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "partner_id": self.env.ref("base.res_partner_4").id,
                    "price": 200000,
                    "property_id": self.properties[0].id,
                }
            )

    def test_garden_reset(self):
        with Form(self.properties[1]) as form:
            form.garden = True
            self.assertEqual(form.garden_area, 10)
            self.assertEqual(form.garden_orientation, "north")

            form.garden = False
            self.assertEqual(form.garden_area, 0, "Garden area should be reset to 0")
            self.assertEqual(
                form.garden_orientation,
                False,
                "Garden orientation should be reset to False",
            )
